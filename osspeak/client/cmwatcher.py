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
        self.active_scope = None
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

    def init_scopes(self):
        for path, cmd_module in self.cmd_modules.items():
            scope_config = cmd_module.config.get('scope', {})
            scope = self.new_or_existing_scope(scope_config)
            cmd_module.scope = scope
            self.scopes.add(scope)
            #TODO: fix later
            self.active_scope = scope

    def create_grammar_nodes(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.load_commands()
            for cmd in cmd_module.commands:
                cmd_module.scope.grammar_node.rules.append(cmd.rule)
                self.command_map[cmd.id] = cmd

    def create_rule_grammar_nodes(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.load_variables()
            for var in cmd_module.variables:
                cmd_module.scope.grammar_node.variables.append(var)

    def load_functions(self):
        for path, cmd_module in self.cmd_modules.items():
            cmd_module.load_functions()          

    def serialize_scope_xml(self, scope):
        converter = SrgsXmlConverter()
        scope.grammar_xml = converter.convert_grammar(scope.grammar_node)

    def new_or_existing_scope(self, config):
        for scope in self.scopes:
            if scope.config_matches(config):
                return scope
        return scopes.Scope(config)

