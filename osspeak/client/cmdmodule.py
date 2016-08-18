import os
import json
import xml.etree.ElementTree as ET
from osspeak.sprecgrammars import astree
from osspeak.sprecgrammars.formats import VocolaParser, SrgsXmlConverter
# print(dir(sprecgrammars.parsers))

class CommandModuleHandler:

    def __init__(self):
        self.cmd_modules = {}

    def load_command_json(self):
        for root, dirs, filenames in os.walk(r'C:\Users\evan\modules\OSSpeak\user\commands'):
            for fname in filenames:
                full_path = os.path.join(root, fname)
                with open(full_path) as f:
                    self.cmd_modules[full_path] = json.load(f)

    def send_grammar_load_message(self, messenger):
        for path, cmd_module_json in self.cmd_modules.items():
            module_string = json.dumps(cmd_module_json)
            print('sending message')
            print('load_command_module {}'.format(module_string))
            messenger.send_message('load_command_module {}'.format(module_string))

    def build_srgs_xml_grammar(self):
        grammar_node = astree.GrammarNode()
        for path, cmd_module in self.cmd_modules.items():
            for cmd in cmd_module['Commands']:
                parser = VocolaParser(cmd)
                rule = parser.parse_as_rule()
                grammar_node.rules.append(rule)
            print(cmd_module)
        converter = SrgsXmlConverter()
        grammar = converter.convert_grammar(grammar_node)
        return grammar
        