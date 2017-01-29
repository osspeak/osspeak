import os
import json
import threading
import collections
import tempfile
from sprecgrammars.actions.parser import ActionParser
import sprecgrammars.functions.library.state
from settings import usersettings
from interfaces.gui import serializer
from client import commands, scopes
from sprecgrammars.rules import astree
from sprecgrammars.rules.parser import RuleParser
from sprecgrammars.rules.converter import SrgsXmlConverter
from platforms import api
from communication import messages
import time

class CommandModuleWatcher:

    def __init__(self):
        self.current_condition = scopes.CurrentCondition()
        self.initial = True
        self.not_loading_modules = threading.Event()
        self.modules_to_save = {}
        self.last_changeset = {}
        self.command_module_json = self.load_command_json()
        self.shutdown = threading.Event()
        messages.subscribe('shutdown', lambda: self.shutdown.set())
        messages.subscribe('perform commands', self.perform_commands)
        messages.subscribe('set saved modules', self.set_saved_modules)

    def load_modules(self, previous_active_modules=None):
        self.initialize_modules()
        self.flag_active_modules()
        self.load_command_module_information()
        self.fire_activation_events(previous_active_modules)
        self.create_grammar_output()
        messages.dispatch('start engine listening',
                          self.initial,
                          self.grammar_xml,
                          self.grammar_node.id)
        self.initial = False

    def initialize_modules(self):
        self.init_fields()
        self.load_command_modules()
        self.load_scope_and_conditions()

    def fire_activation_events(self, previous_active_modules):
        previous_names, current_names = set(previous_active_modules), set(self.active_modules)
        for deactivated_name in previous_names - current_names:
            cmd_module = previous_active_modules[deactivated_name]
            if 'deactivate' in cmd_module.events:
                cmd_module.events['deactivate'].perform(variables=[])
        for activated_name in current_names - previous_names:
            cmd_module = self.active_modules[activated_name]
            if 'activate' in cmd_module.events:
                cmd_module.events['activate'].perform(variables=[])

    def create_grammar_output(self):
        self.send_module_information_to_ui()
        self.serialize_scope_xml()

    def init_fields(self):
        self.conditions = {
            'titles': collections.defaultdict(set),
            'state': None,
        }
        # start with global scope
        self.scope_groupings = {'': scopes.Scope()}
        self.cmd_modules = {}
        self.active_modules = {}
        self.grammar_node = astree.GrammarNode()
        self.grammar_xml = None
        # key is string id, val is Action instance
        self.command_map = {}

    def load_command_json(self):
        json_module_dicts = {}
        command_dir = usersettings.command_directory()
        if not os.path.isdir(command_dir):
            os.makedirs(command_dir)
        for root, dirs, filenames in os.walk(command_dir):
            # skip hidden directories such as .git
            dirs[:] = sorted([d for d in dirs if not d.startswith('.')])
            self.load_json_directory(filenames, command_dir, root, json_module_dicts)
        return json_module_dicts

    def load_json_directory(self, filenames, command_dir, root, json_module_dicts):
        for fname in filenames:
            if not fname.endswith('.json'):
                continue
            full_path = os.path.join(root, fname)
            partial_path = full_path[len(command_dir) + 1:]
            with open(full_path) as f:
                try:
                    module_config = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    module_config = {'Error': str(e)}
                json_module_dicts[partial_path] = module_config

    def load_command_modules(self):
        for path, config in self.command_module_json.items():
            cmd_module = commands.CommandModule(config, path)
            self.cmd_modules[path] = cmd_module

    def load_scope_and_conditions(self):
        for path, cmd_module in self.cmd_modules.items():
            self.load_conditions(path, cmd_module)
            self.load_scope(path, cmd_module)

    def load_initial_user_state(self):
        for path, cmd_module in self.cmd_modules.items():
            initial_state = {k: eval(v) for k, v in cmd_module.initial_state.items()}
            sprecgrammars.functions.library.state.USER_DEFINED_STATE.update(initial_state)

    def flag_active_modules(self):
        for path, cmd_module in self.get_active_modules():
            self.active_modules[path] = cmd_module

    def get_active_modules(self):
        for path, cmd_module in self.cmd_modules.items():
            is_active = self.is_command_module_active(cmd_module)
            if is_active:
                yield path, cmd_module

    def is_command_module_active(self, cmd_module):
        return self.current_window_matches(cmd_module) and cmd_module.state

    def current_window_matches(self, cmd_module):
        for title_filter, filtered_paths in self.conditions['titles'].items():
            if cmd_module.path in filtered_paths:
                if title_filter in self.current_condition.window_title:
                    return True
                return False
        return True

    def load_command_module_information(self):
        self.load_functions()
        self.load_rules()
        self.load_commands()
        self.load_events()

    def load_functions(self):
        self.load_builtin_functions()
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.define_functions()
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.set_function_actions()

    def load_rules(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.initialize_rules()
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.load_rules()
            for rule in cmd_module.rules:
                if path in self.active_modules:
                    self.grammar_node.rules.append(rule)

    def load_commands(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.load_commands()
            for cmd in cmd_module.commands:
                self.command_map[cmd.id] = cmd
                if path in self.active_modules:
                    self.grammar_node.rules.append(cmd.rule)
    
    def load_builtin_functions(self):
        from sprecgrammars.api import rule
        global_scope = self.scope_groupings['']
        global_scope._rules['_dictate'] = rule('', '_dictate')

    def load_events(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.load_events()

    def serialize_scope_xml(self):
        converter = SrgsXmlConverter()
        self.grammar_xml = converter.convert_grammar(self.grammar_node)

    def load_conditions(self, path, cmd_module):
        conditions_config = cmd_module.conditions
        title = conditions_config.get('title', '').lower()
        if title:
            self.conditions['titles'][title].add(path)

    def load_scope(self, path, cmd_module):
        scope_name = cmd_module.config.get('scope', '')
        if scope_name not in self.scope_groupings:
            global_scope = self.scope_groupings['']
            self.scope_groupings[scope_name] = scopes.Scope(global_scope, name=scope_name)
        self.scope_groupings[scope_name].cmd_modules[path] = cmd_module
        cmd_module.scope = self.scope_groupings[scope_name]

    def start_watch_active_window(self):
        self.load_initial_user_state()
        t = threading.Thread(target=self.watch_active_window)
        t.start()

    def watch_active_window(self):
        current_user_state = sprecgrammars.functions.library.state.USER_DEFINED_STATE.copy()
        while not self.shutdown.isSet():
            changed_modules = self.save_updated_modules()
            if changed_modules:
                self.update_modules(changed_modules)
                continue
            current_user_state = self.maybe_load_modules(current_user_state)
            self.shutdown.wait(timeout=1)

    def save_updated_modules(self):
        # should use a lock here
        modules_to_save = self.modules_to_save
        self.modules_to_save = {}
        changed_modules = {}
        for path, cmd_module_config in modules_to_save.items():
            if cmd_module_config != self.cmd_modules[path].config:
                changed_modules[path] = cmd_module_config
        return changed_modules

    def maybe_load_modules(self, current_user_state):
        active_window = api.get_active_window_name().lower()
        if active_window == self.current_condition.window_title and current_user_state == sprecgrammars.functions.library.state.USER_DEFINED_STATE:
            return current_user_state
        current_user_state = sprecgrammars.functions.library.state.USER_DEFINED_STATE.copy()
        self.current_condition.window_title = active_window
        new_active_modules = dict(self.get_active_modules())
        if new_active_modules != self.active_modules:
            self.load_modules(self.active_modules)
        return current_user_state

    def update_modules(self, modified_modules):
        command_dir = usersettings.command_directory()
        for path, cmd_module_config in modified_modules.items():
            self.command_module_json[path] = cmd_module_config
            with open(os.path.join(command_dir, path), 'w') as outfile:
                json.dump(cmd_module_config, outfile, indent=4)
        self.load_modules()

    def save_updated_modules(self):
        # should use a lock here
        modules_to_save = self.modules_to_save
        self.modules_to_save = {}
        changed_modules = {}
        for path, cmd_module_config in modules_to_save.items():
            if cmd_module_config != self.cmd_modules[path].config:
                changed_modules[path] = cmd_module_config
        return changed_modules

    def save_changed_modules(self):
        self.changed_modules = {'created': {}, 'edited': {}, 'deleted': {}, 'all': self.cmd_modules}

    def send_module_information_to_ui(self):
        payload = {'modules': self.cmd_modules}
        messages.dispatch('load module map', payload)

    def set_saved_modules(self, modules_to_save):
        self.modules_to_save = modules_to_save

    def perform_commands(self, grammar_id, commands):
        if grammar_id != self.grammar_node.id:
            return
        for cmd_recognition in commands:
            cmd = self.command_map[cmd_recognition['RuleId']]
            cmd.perform_action(cmd_recognition)