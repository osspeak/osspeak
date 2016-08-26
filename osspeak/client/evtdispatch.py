import xml.etree.ElementTree as ET
from osspeak.communication.engines import ProcessManager
from osspeak.client import cmdmodule

class EventDispatcher:

    def __init__(self):
        self.start_engine_process()
        self.start_module_watcher()

    def start_engine_process(self):
        self.engine_process = ProcessManager(self)
        self.engine_process.start_stdout_listening()

    def start_module_watcher(self):
        self.cmd_module_watcher = cmdmodule.CommandModuleWatcher()
        self.cmd_module_watcher.load_command_json()
        self.cmd_module_watcher.create_grammar_nodes()
        grammar = self.cmd_module_watcher.build_srgs_xml_grammar()
        msg = 'grammar_content {}'.format(ET.tostring(grammar).decode('utf8'))
        self.engine_process.send_message(msg)
        input('Press the any key: ')

    def main_loop(self):
        input()