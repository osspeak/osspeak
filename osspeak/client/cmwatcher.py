import itertools
import uuid
import os
import collections
import json
import log
import sprecgrammars.functions.library.state
from user import settings
from interfaces.gui import serializer
from client import commands, scopes, action, userstate, variables
from sprecgrammars.rules.converter import SrgsXmlConverter
from platforms import api
import xml.etree.ElementTree as ET
from communication import messages

class CommandModuleWatcher:

    def __init__(self):
        self.grammar_commands = collections.OrderedDict() # grammar_id: string -> dictionary of commands
        self.modules_to_save = {}
        self.command_module_json = self.load_command_json()
        messages.subscribe(messages.PERFORM_COMMANDS, self.perform_commands)
        messages.subscribe(messages.SET_SAVED_MODULES, self.update_modules)

    def load_modules(self, current_window, current_state, reload_files=False):
        previous_active_modules = self.active_modules
        if reload_files:
            self.load_initial_user_state()
            self.command_module_json = self.load_command_json()
        self.initialize_modules()
        self.active_modules = self.get_active_modules(current_window, current_state)
        self.load_command_module_information()
        self.fire_activation_events(previous_active_modules)
        self.send_module_information_to_ui()
        self.load_and_send_grammar()

    def load_and_send_grammar(self):
        active_rules = self.active_rules
        node_ids = self.generate_node_ids(active_rules)
        commands = self.active_commands
        grammar_commands = {}
        for cmd in commands:
            variable_tree = variables.RecognitionResultsTree(cmd.rule, node_ids)
            grammar_commands[node_ids[cmd.rule]] = {'command': cmd, 'variable_tree': variable_tree}
        grammar_xml = self.build_grammar_xml(active_rules, node_ids)
        grammar_id = str(uuid.uuid4())
        self.add_new_grammar(grammar_commands, grammar_id)
        messages.dispatch(messages.LOAD_GRAMMAR, ET.tostring(grammar_xml).decode('utf8'), grammar_id)

    def add_new_grammar(self, commands, grammar_id):
        # remove oldest grammar if needed
        if len(self.grammar_commands) > 4:
            self.grammar_commands.popitem(last=False)
        self.grammar_commands[grammar_id] = commands

    def generate_node_ids(self, rules):
        from sprecgrammars.rules import astree
        prefix_map = {astree.GroupingNode: 'g', astree.Rule: 'r', astree.WordNode: 'w'}
        node_ids = {}
        for rule in rules:
            for node in rule.walk():
                if node not in node_ids:
                    prefix = prefix_map.get(type(node), 'n')
                    node_ids[node] = f'{prefix}{len(node_ids) + 1}'
        return node_ids

    def initialize_modules(self):
        self.init_fields()
        self.load_command_modules()
        self.load_scopes()

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

    def init_fields(self):
        # start with global scope
        self.scope_groupings = {'': scopes.Scope()}
        self.cmd_modules = {}
        self.active_modules = {}

    def load_command_json(self):
        json_module_dicts = {}
        command_dir = settings.user_settings['command_directory']
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
            log.logger.debug(f"Loading command module '{partial_path}'...")
            with open(full_path) as f:
                try:
                    module_config = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    module_config = {'Error': str(e)}
                    log.logger.warning(f"JSON error loading command module '{partial_path}':\n{e}")
                json_module_dicts[partial_path] = module_config

    def load_command_modules(self):
        for path, config in self.command_module_json.items():
            self.cmd_modules[path] = commands.CommandModule(config, path)

    def load_scopes(self):
        for path, cmd_module in self.cmd_modules.items():
            scope_name = cmd_module.config.get('scope', '')
            if scope_name not in self.scope_groupings:
                global_scope = self.scope_groupings['']
                self.scope_groupings[scope_name] = scopes.Scope(global_scope, name=scope_name)
            self.scope_groupings[scope_name].cmd_modules[path] = cmd_module
            cmd_module.scope = self.scope_groupings[scope_name]

    def load_initial_user_state(self):
        sprecgrammars.functions.library.state.USER_DEFINED_STATE = {}
        for path, cmd_module in self.cmd_modules.items():
            initial_state = {k: eval(v) for k, v in cmd_module.initial_state.items()}
            sprecgrammars.functions.library.state.USER_DEFINED_STATE.update(initial_state)

    def get_active_modules(self, current_window, current_state):
        active_modules = {}
        for path, cmd_module in self.cmd_modules.items():
            if self.is_command_module_active(cmd_module, current_window, current_state):
                active_modules[path] = cmd_module
        return active_modules

    def is_command_module_active(self, cmd_module, current_window, current_state):
        title_filter = cmd_module.conditions.get('title')
        current_window_matches = title_filter is None or title_filter.lower() in current_window.lower() 
        return current_window_matches and cmd_module.state_active(current_state)

    def load_command_module_information(self):
        self.load_functions()
        self.load_rules()
        self.load_commands()
        self.load_events()

    def load_functions(self):
        self.load_builtin_functions()
        for cmd_module in self.cmd_modules.values():
            cmd_module.define_functions()
        for cmd_module in self.cmd_modules.values():
            cmd_module.set_function_actions()

    def load_rules(self):
        for cmd_module in self.cmd_modules.values():
            cmd_module.initialize_rules()
        for cmd_module in self.cmd_modules.values():
            cmd_module.load_rules()

    def load_commands(self):
        for cmd_module in self.cmd_modules.values():
            cmd_module.load_commands()
    
    def load_builtin_functions(self):
        from sprecgrammars.api import rule
        global_scope = self.scope_groupings['']
        global_scope.rules['_dictate'] = rule('', '_dictate')

    def load_events(self):
        for cmd_module in self.cmd_modules.values():
            cmd_module.load_events()

    def build_grammar_xml(self, active_rules, node_ids):
        return SrgsXmlConverter(node_ids).build_grammar(active_rules)

    @property
    def active_rules(self):
        rules = []
        command_rules = []
        for cmd_module in self.active_modules.values():
            rules.extend(cmd_module.rules)
            command_rules.extend(cmd.rule for cmd in cmd_module.commands)
        rules.extend(command_rules)
        return rules

    @property
    def active_commands(self):
        grouped_commands = [m.commands for m in self.active_modules.values()]
        return list(itertools.chain.from_iterable(grouped_commands))

    def update_modules(self, modified_modules):
        raise NotImplementedError
        command_dir = settings.user_settings['command_directory']
        for path, cmd_module_config in modified_modules.items():
            self.command_module_json[path] = cmd_module_config
            with open(os.path.join(command_dir, path), 'w') as outfile:
                json.dump(cmd_module_config, outfile, indent=4)
        self.load_modules()

    def send_module_information_to_ui(self):
        payload = {'modules': self.cmd_modules}
        messages.dispatch(messages.LOAD_MODULE_MAP, payload)

    def perform_commands(self, command_results, grammar_id):
        try:
            command_map = self.grammar_commands[grammar_id]
        except KeyError:
            log.logger.warning(f'Grammar {grammar_id} no longer exists')
            return
        action.perform_commands(command_results, command_map)