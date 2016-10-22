import os
import json
import collections
import tempfile
import xml.etree.ElementTree as ET
from sprecgrammars.actions.parser import ActionParser
from settings import usersettings
from client import commands
from sprecgrammars.formats.rules import astree
from sprecgrammars.formats import RuleParser, SrgsXmlConverter

class CommandModuleWatcher:

    def __init__(self):
        self.cmd_modules = {}
        self.active_scope = None
        # key is string id, val is Action instance
        self.command_map = {}
        self.grammar_nodes = collections.defaultdict(self.init_scope_grammars)

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

    def create_grammar_nodes(self):
        for path, cmd_module in self.cmd_modules.items():
            scope = cmd_module.config.get('scope')
            scope_info = self.grammar_nodes[scope]
            cmd_module.load_commands(scope_info['variables'])
            grammar = scope_info['main grammar']['node']
            for cmd in cmd_module.commands:
                grammar.rules.append(cmd.rule)
                self.command_map[cmd.id] = cmd

    def create_rule_grammar_nodes(self):
        for path, cmd_module in self.cmd_modules.items():
            scope = cmd_module.config.get('scope')
            scope_info = self.grammar_nodes[scope]
            cmd_module.load_variables(scope_info['variables'])
            grammar = scope_info['main grammar']['node']
            for var in cmd_module.variables:
                grammar.variables.append(var)

    def init_scope_grammars(self):
        return {
            'main grammar': {'node': astree.GrammarNode(), 'xml': None},
            'variables': {},
        }

    def build_srgs_xml_grammar(self, scope):
        grammar_node = self.grammar_nodes[scope]['main grammar']['node']
        converter = SrgsXmlConverter()
        grammar = converter.convert_grammar(grammar_node)
        return grammar

    def serialize_scope_xml(self, scope):
        scope_info = self.grammar_nodes[scope]
        for grammar_name in ('main',):
            gramkey = '{} grammar'.format(grammar_name)
            grammar_node = scope_info[gramkey]['node']
            converter = SrgsXmlConverter()
            scope_info[gramkey]['xml'] = converter.convert_grammar(grammar_node)

