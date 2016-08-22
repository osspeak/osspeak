import os
import json
import collections
import xml.etree.ElementTree as ET
from osspeak.sprecgrammars.actions.parser import ActionParser
from osspeak.sprecgrammars import astree
from osspeak.sprecgrammars.formats import VocolaParser, SrgsXmlConverter
# print(dir(sprecgrammars.parsers))

class CommandModuleHandler:

    def __init__(self):
        self.cmd_modules = {}
        # key is string id, val is Action instance
        self.actions = {}
        self.grammar_nodes = {}

    def load_command_json(self):
        for root, dirs, filenames in os.walk(r'C:\Users\evan\modules\OSSpeak\user\commands'):
            for fname in filenames:
                full_path = os.path.join(root, fname)
                with open(full_path) as f:
                    cmd_module = json.load(f)
                    self.cmd_modules[full_path] = cmd_module

    def create_grammar_nodes(self):
        for path, cmd_module in self.cmd_modules.items():
            scope = cmd_module.get('scope')
            grammar = self.grammar_nodes.get(scope, astree.GrammarNode())
            for cmd, action_text in cmd_module['Commands']:
                parser = VocolaParser(cmd)
                rule = parser.parse_as_rule()
                grammar.rules.append(rule)
                self.actions[rule.id] = self.create_action(action_text)
            self.grammar_nodes[scope] = grammar

    def build_srgs_xml_grammar(self):
        grammar_node = self.grammar_nodes[None]
        converter = SrgsXmlConverter()
        grammar = converter.convert_grammar(grammar_node)
        return grammar

    def create_action(self, text):
        parser = ActionParser(text)
        return parser.parse()
        