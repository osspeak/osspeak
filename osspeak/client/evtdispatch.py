import json
import xml.etree.ElementTree as ET
from communication.engines import ProcessManager
from client import cmdmodule

class EventDispatcher:

    def __init__(self):
        self.start_engine_process()
        self.start_module_watcher()
        self.start_engine_listening()

    def start_engine_process(self):
        self.engine_process = ProcessManager(on_output=self.on_engine_message)
        self.engine_process.start_stdout_listening()

    def start_module_watcher(self):
        self.cmd_module_watcher = cmdmodule.CommandModuleWatcher()
        self.cmd_module_watcher.load_command_json()
        self.cmd_module_watcher.create_rule_grammar_nodes()
        self.cmd_module_watcher.create_grammar_nodes()
        self.cmd_module_watcher.serialize_scope_xml(None)

    def start_engine_listening(self):
        scope_info = self.cmd_module_watcher.grammar_nodes[self.cmd_module_watcher.active_scope]
        msg = {
            'Type': 'load grammars',
            'Grammars': {
                'foo': ET.tostring(scope_info['main grammar']['xml']).decode('utf8'),
                # 'bar': ET.tostring(scope_info['variable grammar']['xml']).decode('utf8'),
            },
            'Init': True,
        }
        self.engine_process.send_message(json.dumps(msg))

    def on_engine_message(self, msg):
        parsed_message = json.loads(msg)
        if parsed_message['Type'] == 'recognition': 
            print(parsed_message)
            for cmd_recognition in parsed_message['Commands']:
                cmd = self.cmd_module_watcher.command_map[cmd_recognition['RuleId']]
                cmd.perform_action(cmd_recognition)
        elif parsed_message['Type'] == 'error':
            print('error!')
            print(parsed_message)

    def main_loop(self):
        input()