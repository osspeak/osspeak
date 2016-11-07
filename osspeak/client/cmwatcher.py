import os
import json
import collections
import tempfile
import xml.etree.ElementTree as ET
from sprecgrammars.actions.parser import ActionParser
from settings import usersettings
from client import commands, scopes
from sprecgrammars.formats.rules import astree
from sprecgrammars.formats import RuleParser, SrgsXmlConverter

class CommandModuleWatcher:

    def __init__(self):
        self.cmd_modules = {}
        self.active_scope = scopes.Scope()
        # key is string id, val is Action instance
        self.command_map = {}
        self.scopes = set()

    def load_command_json(self):
        command_dir = usersettings.command_directory()
        if not os.path.isdir(command_dir):
            os.makedirs(command_dir)
        for root, dirs, filenames in os.walk(command_dir):
            for fname in filenames:
                full_path = os.path.join(root, fname)
                with open(full_path) as f:
                    cmd_module = commands.CommandModule(json.load(f))
                    self.cmd_modules[full_path] = cmd_module

    def flag_active_modules(self):
        for path, cmd_module in self.cmd_modules.items():
            scope_config = cmd_module.config.get('scope', {})
            cmd_module.is_active = self.is_command_module_active(scope_config)
            if cmd_module.is_active:
                cmd_module.scope = self.active_scope

    def create_grammar_nodes(self):
        for path, cmd_module in self.cmd_modules.items():
            if cmd_module.is_active:
                cmd_module.load_commands()
                for cmd in cmd_module.commands:
                    self.active_scope.grammar_node.rules.append(cmd.rule)
                    self.command_map[cmd.id] = cmd

    def create_rule_grammar_nodes(self):
        for path, cmd_module in self.cmd_modules.items():
            if cmd_module.is_active:
                cmd_module.load_variables()
                for var in cmd_module.variables:
                    self.active_scope.grammar_node.variables.append(var)
                    self.active_scope.variables[var.name] = var

    def load_functions(self):
        for path, cmd_module in self.cmd_modules.items():
            if cmd_module.is_active:
                cmd_module.load_functions()
                for func in cmd_module.functions:
                    self.active_scope.functions[func.name] = func

    def serialize_scope_xml(self):
        converter = SrgsXmlConverter()
        self.active_scope.grammar_xml = converter.convert_grammar(self.active_scope.grammar_node)

    def is_command_module_active(self, config):
        return True
