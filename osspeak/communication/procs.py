import subprocess
import threading
import json
import sys
import xml.etree.ElementTree as ET
from communication import cmdmodule, messages

if getattr(sys, 'frozen', False):
    ENGINE_PATH = r'engines\wsr\RecognizerIO.exe'
else:
    ENGINE_PATH = r'..\engines\RecognizerIO\RecognizerIO\bin\Debug\RecognizerIO.exe'

class ProcessManager:

    def __init__(self, path, on_output=lambda x: None):
        self.process = subprocess.Popen(path, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        self.on_output = on_output
        self.start_stdout_listening()
        
    def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
        self.process.stdin.write(msg)
        try:
            self.process.stdin.flush()
        except OSError:
            print(f'Process {self} already closed')

    def dispatch_process_output(self):
        for line in self.process.stdout:
            line = line.decode('utf8')
            self.on_output(line)

    def start_stdout_listening(self):
        t = threading.Thread(target=self.dispatch_process_output, daemon=True)
        t.start()

class EngineProcessManager(ProcessManager):

    def __init__(self, remote=False):
        super().__init__(ENGINE_PATH, on_output=self.on_engine_message)
        messages.subscribe(messages.START_ENGINE_LISTENING, self.start_engine_listening)
        messages.subscribe(messages.ENGINE_STOP, self.stop)
        messages.subscribe(messages.STOP_MAIN_PROCESS , self.shutdown)
        messages.subscribe(messages.EMULATE_RECOGNITION, self.emulate_recognition)
        
    def send_message(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        super().send_message(msg)

    def start_engine_listening(self, init, grammar_xml, grammar_id):
        msg = {
            'Type': 'load grammars',
            'Grammars': {
                grammar_id: grammar_xml,
            },
            'Init': init,
        }
        self.send_message(msg)

    def on_engine_message(self, msg_string):
        msg = json.loads(msg_string)
        if msg['Type'] == 'recognition':
            messages.dispatch(messages.PERFORM_COMMANDS, msg['GrammarId'], msg['Commands'])
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
