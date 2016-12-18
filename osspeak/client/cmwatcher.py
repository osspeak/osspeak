import os
import json
import threading
import collections
import tempfile
import xml.etree.ElementTree as ET
from sprecgrammars.actions.parser import ActionParser
from settings import usersettings
from interfaces.gui import serializer
from client import commands, scopes
from sprecgrammars.formats.rules import astree
from sprecgrammars.formats import RuleParser, SrgsXmlConverter
from platforms import api
import time

class CommandModuleWatcher:

    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.current_condition = scopes.CurrentCondition()
        self.initial = True
        self.modules_to_save = {}
        self.raw_command_text_files = self.load_command_json()

    def load_modules(self):
        self.initialize_modules()
        self.display_module_tree()
        self.create_grammar_output()
        self.event_dispatcher.engine_process.start_engine_listening(init=self.initial)
        self.initial = False

    def initialize_modules(self):
        self.init_fields()
        self.load_command_modules()
        self.load_scope_and_conditions()
        self.flag_active_modules()

    def create_grammar_output(self):
        self.load_functions()
        self.load_variables()
        self.load_commands()
        self.send_module_information()
        self.serialize_scope_xml()

    def init_fields(self):
        self.conditions = {
            'titles': collections.defaultdict(set),
            'variables': collections.defaultdict(set),
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
        raw_command_text_files = {}
        command_dir = usersettings.command_directory()
        if not os.path.isdir(command_dir):
            os.makedirs(command_dir)
        for root, dirs, filenames in os.walk(command_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in filenames:
                if not fname.endswith('.json'):
                    continue
                full_path = os.path.join(root, fname)
                partial_path = full_path[len(command_dir) + 1:]
                with open(full_path) as f:
                    raw_command_text_files[partial_path] = json.load(f)
        return raw_command_text_files

    def load_command_modules(self):
        for path, config in self.raw_command_text_files.items():
            cmd_module = commands.CommandModule(config, path)
            self.cmd_modules[path] = cmd_module

    def load_scope_and_conditions(self):
        for path, cmd_module in self.cmd_modules.items():
            self.load_conditions(path, cmd_module)
            self.load_scope(path, cmd_module)

    def flag_active_modules(self):
        for path, cmd_module in self.get_active_modules():
            self.active_modules[path] = cmd_module

    def get_active_modules(self):
        for path, cmd_module in self.cmd_modules.items():
            is_active = self.is_command_module_active(cmd_module)
            if is_active:
                yield path, cmd_module

    def is_command_module_active(self, cmd_module):
        for title_filter, filtered_paths in self.conditions['titles'].items():
            if cmd_module.path in filtered_paths:
                if title_filter in self.current_condition.window_title:
                    return True
                return False
        return True

    def load_functions(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.define_functions()
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.set_function_actions()

    def load_variables(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.initialize_variables()
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.load_variables()
            for var in cmd_module.variables:
                if path in self.active_modules:
                    self.grammar_node.variables.append(var)

    def load_commands(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.load_commands()
            for cmd in cmd_module.commands:
                self.command_map[cmd.id] = cmd
                if path in self.active_modules:
                    self.grammar_node.rules.append(cmd.rule)

    def serialize_scope_xml(self):
        converter = SrgsXmlConverter()
        self.grammar_xml = converter.convert_grammar(self.grammar_node)

    def load_conditions(self, path, cmd_module):
        conditions_config = cmd_module.config.get('Conditions', {})
        title = conditions_config.get('Title', '').lower()
        if title:
            self.conditions['titles'][title].add(path)

    def load_scope(self, path, cmd_module):
        scope_name = cmd_module.config.get('Scope', '')
        if scope_name not in self.scope_groupings:
            global_scope = self.scope_groupings['']
            self.scope_groupings[scope_name] = scopes.Scope(global_scope, name=scope_name)
        self.scope_groupings[scope_name].cmd_modules[path] = cmd_module
        cmd_module.scope = self.scope_groupings[scope_name]

    def start_watch_active_window(self):
        t = threading.Thread(target=self.watch_active_window)
        t.start()

    def watch_active_window(self):
        import time
        while True:
            time.sleep(2)
            changed_modules = self.save_updated_modules()
            if changed_modules:
                self.update_modules(changed_modules)
                continue
            active_window = api.get_active_window_name().lower()
            if active_window != self.current_condition.window_title:
                self.current_condition.window_title = active_window
                new_active_modules = dict(self.get_active_modules())
                if new_active_modules != self.active_modules or self.initial:
                    self.load_modules()

    def update_modules(self, modified_modules):
        command_dir = usersettings.command_directory()
        for path, cmd_module_config in modified_modules.items():
            self.raw_command_text_files[path] = cmd_module_config
            with open(os.path.join(command_dir, path), 'w') as outfile:
                json.dump(cmd_module_config, outfile)
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

    def display_module_tree(self):
        tree = self.serialize_as_tree()
        payload = {'tree': tree}
        if self.initial:
            self.event_dispatcher.gui_manager.send_message('display module tree',
                payload, encoder=serializer.GuiEncoder)

    def send_module_information(self):
        payload = {'modules': self.cmd_modules}
        self.event_dispatcher.gui_manager.send_message('module map',
            payload, encoder=serializer.GuiEncoder)

    def serialize_as_tree(self):
        node_map = {'': {'children': []}}
        command_dir = usersettings.command_directory()
        for path, cmd_module in self.cmd_modules.items():
            tree_path = list(os.path.split(path))
            if tree_path[0] == '':
                tree_path.pop(0)
            self.add_tree_node(tree_path, node_map, cmd_module)
        return node_map['']['children']

    def add_tree_node(self, path, node_map, cmd_module):
        parent = node_map['']['children']
        partial_path = ''
        for directory in path[:-1]:
            partial_path += os.sep + directory
            if partial_path not in node_map:
                node = {'text': directory, 'children': [], 'id': partial_path}
                node_map[partial_path] = node
                parent.append(node)
            parent = node_map[partial_path]['children']
        parent.append({'text': path[-1], 'id': os.path.join(*path)})