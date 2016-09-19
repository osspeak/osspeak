import os
import json
import collections
import xml.etree.ElementTree as ET
from sprecgrammars.actions.parser import ActionParser
from client import commands
from sprecgrammars import astree
from sprecgrammars.formats import VocolaParser, SrgsXmlConverter

class CommandModuleWatcher:

    def __init__(self):
        self.cmd_modules = {}
        # key is string id, val is Action instance
        self.command_map = {}
        self.grammar_nodes = {}

    def load_command_json(self):
        for root, dirs, filenames in os.walk(r'C:\Users\evan\modules\OSSpeak\user\commands'):
            for fname in filenames:
                full_path = os.path.join(root, fname)
                with open(full_path) as f:
                    cmd_module = commands.CommandModule(json.load(f))
                    cmd_module.load_commands()
                    self.cmd_modules[full_path] = cmd_module

    def create_grammar_nodes(self):
        for path, cmd_module in self.cmd_modules.items():
            scope = cmd_module.config.get('scope')
            grammar = self.grammar_nodes.get(scope, astree.GrammarNode())
            for cmd in cmd_module.commands:
                grammar.rules.append(cmd.rule)
                self.command_map[cmd.id] = cmd
            self.grammar_nodes[scope] = grammar

    def build_srgs_xml_grammar(self):
        grammar_node = self.grammar_nodes[None]
        converter = SrgsXmlConverter()
        grammar = converter.convert_grammar(grammar_node)
        return grammar
