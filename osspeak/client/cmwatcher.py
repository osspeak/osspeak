import os
import json
import threading
import collections
import tempfile
import xml.etree.ElementTree as ET
from sprecgrammars.actions.parser import ActionParser
from settings import usersettings
from client import commands, scopes
from sprecgrammars.formats.rules import astree
from sprecgrammars.formats import RuleParser, SrgsXmlConverter
from platforms import api

class CommandModuleWatcher:

    def __init__(self):
        pass

    def create_grammar_output(self):
        self.init_fields()
        self.load_command_json()
        self.load_scope_and_conditions()
        self.flag_active_modules()
        self.load_functions()
        self.create_rule_grammar_nodes()
        self.create_grammar_nodes()
        self.serialize_scope_xml()

    def init_fields(self):
        self.current_condition = scopes.CurrentCondition()
        self.conditions = {
            'titles': collections.defaultdict(set),
            'variables': collections.defaultdict(set),
        }
        # start with global scope
        self.scope_groupings = {'': scopes.Scope2()}
        self.cmd_modules = {}
        self.active_modules = {}
        self.active_scope = scopes.Scope()
        self.grammar_node = astree.GrammarNode()
        # key is string id, val is Action instance
        self.command_map = {}

    def load_command_json(self):
        command_dir = usersettings.command_directory()
        if not os.path.isdir(command_dir):
            os.makedirs(command_dir)
        for root, dirs, filenames in os.walk(command_dir):
            for fname in filenames:
                full_path = os.path.join(root, fname)
                with open(full_path) as f:
                    cmd_module = commands.CommandModule(json.load(f), full_path)
                    self.cmd_modules[full_path] = cmd_module

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

    def create_grammar_nodes(self):
        for path, cmd_module in self.active_modules.items():
            cmd_module.load_commands()
            for cmd in cmd_module.commands:
                self.grammar_node.rules.append(cmd.rule)
                self.command_map[cmd.id] = cmd

    def create_rule_grammar_nodes(self):
        for path, cmd_module in self.active_modules.items():
            cmd_module.load_variables()
            for var in cmd_module.variables:
                self.grammar_node.variables.append(var)

    def load_functions(self):
        for path, cmd_module in self.active_modules.items():
            cmd_module.load_functions()

    def serialize_scope_xml(self):
        converter = SrgsXmlConverter()
        self.active_scope.grammar_xml = converter.convert_grammar(self.grammar_node)

    def is_command_module_active(self, cmd_module):
        for title_filter, filtered_paths in self.conditions['titles'].items():
            if cmd_module.path in filtered_paths:
                if title_filter in self.active_scope.current_window_title:
                    return True
                return False
        return True

    def load_conditions(self, path, cmd_module):
        conditions_config = cmd_module.config.get('Conditions', {})
        title = conditions_config.get('Title', '').lower()
        if title:
            self.conditions['titles'][title].add(path)

    def load_scope(self, path, cmd_module):
        scope_name = cmd_module.config.get('Scope', '')
        if scope_name not in self.scope_groupings:
            global_scope = self.scope_groupings['']
            self.scope_groupings[scope_name] = scopes.Scope2(global_scope)
        self.scope_groupings[scope_name].cmd_modules[path] = cmd_module
        cmd_module.scope = self.scope_groupings[scope_name]

    def start_watch_active_window(self, on_change):
        t = threading.Thread(target=self.watch_active_window, args=(on_change,))
        t.start()

    def watch_active_window(self, on_change):
        import time
        while True:
            time.sleep(2)
            active_window = api.get_active_window_name().lower()
            if active_window != self.active_scope.current_window_title:
                self.active_scope.current_window_title = active_window
                self.create_grammar_output()
                on_change(init=False)