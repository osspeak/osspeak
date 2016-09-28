import json
import xml.etree.ElementTree as ET
from communication.engines import ProcessManager
from client import cmdmodule

class EventDispatcher:

    def __init__(self):
        self.start_engine_process()
        self.start_module_watcher()

    def start_engine_process(self):
        self.engine_process = ProcessManager(on_output=self.on_engine_message)
        self.engine_process.start_stdout_listening()

    def start_module_watcher(self):
        self.cmd_module_watcher = cmdmodule.CommandModuleWatcher()
        self.cmd_module_watcher.load_command_json()
        self.cmd_module_watcher.create_rule_grammar_nodes()
        self.cmd_module_watcher.create_grammar_nodes()
        grammar = self.cmd_module_watcher.build_srgs_xml_grammar()
        msg = 'grammar_content {}'.format(ET.tostring(grammar).decode('utf8'))
        self.engine_process.send_message(msg)

    def on_engine_message(self, msg):
        parsed_message = json.loads(msg)
        print(parsed_message)
        if parsed_message['Type'] == 'result': 
            cmd = self.cmd_module_watcher.command_map[parsed_message['RuleId']]
            cmd.perform_action(parsed_message)

    def main_loop(self):
        input()