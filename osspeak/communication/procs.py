import subprocess
import threading
import json
import sys
import xml.etree.ElementTree as ET

if getattr(sys, 'frozen', False):
    ENGINE_PATH = r'engines\wsr\RecognizerIO.exe'
else:
    ENGINE_PATH = r'..\engines\RecognizerIO\RecognizerIO\bin\Debug\RecognizerIO.exe'

class ProcessManager:

    def __init__(self, path, on_output=lambda x: None):
        self.process = subprocess.Popen(path, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.on_output = on_output
        
    def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
        self.process.stdin.write(msg)
        self.process.stdin.flush()

    def dispatch_process_output(self):
        for line in self.process.stdout:
            line = line.decode('utf8')
            self.on_output(line)

    def start_stdout_listening(self):
        t = threading.Thread(target=self.dispatch_process_output)
        t.start()

class EngineProcessManager(ProcessManager):

    def __init__(self, cmd_module_watcher):
        super().__init__(ENGINE_PATH, on_output=self.on_engine_message)
        self.cmd_module_watcher = cmd_module_watcher
        
    def send_message(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        super().send_message(msg)

    def start_engine_listening(self, init=True):
        grammar_xml = self.cmd_module_watcher.grammar_xml
        msg = {
            'Type': 'load grammars',
            'Grammars': {
                id(grammar_xml): ET.tostring(grammar_xml).decode('utf8'),
            },
            'Init': init,
        }
        self.send_message(msg)

    def on_engine_message(self, msg_string):
        msg = json.loads(msg_string)
        if msg['Type'] == 'recognition': 
            print(msg)
            for cmd_recognition in msg['Commands']:
                cmd = self.cmd_module_watcher.command_map[cmd_recognition['RuleId']]
                cmd.perform_action(cmd_recognition)
        elif msg['Type'] == 'error':
            print('error!')
            print(msg['Message'])

    def send_simple_message(self, msg_type):
        self.send_message({'Type': msg_type})        

    def shutdown(self):
        self.send_simple_message('shutdown')

    def stop(self):
        self.send_simple_message('stop')

    def start(self):
        self.send_simple_message('start')

    def emulate_recognition(self, text, delay=5):
        msg = {
            'Type': 'emulate recognition',
            'Delay': delay,
            'Text': text
        }
        self.send_message(msg)
