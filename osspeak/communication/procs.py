import time
import asyncio
import asyncio.subprocess
import subprocess
import threading
import json
import sys
from user.settings import user_settings
import xml.etree.ElementTree as ET
from communication import messages, pubsub, topics

if getattr(sys, 'frozen', False):
    ENGINE_PATH = r'engines\wsr\RecognizerIO.exe'
else:
    ENGINE_PATH = r'..\engines\RecognizerIO\RecognizerIO\bin\Debug\RecognizerIO.exe'

class ProcessManager:

    @classmethod
    async def create(cls, path, *a, **kw):
        process_instance = cls(path, *a, **kw)
        create = asyncio.create_subprocess_exec(
            path,
            stdout=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        process_instance.process = await create
        asyncio.ensure_future(process_instance.dispatch_process_output())


    def __init__(self, path, on_output=lambda x: None, on_exit=lambda: None):
        self.on_output = on_output
        self.on_exit = on_exit
        self.process = None
        
    async def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
        self.process.stdin.write(msg)
        try:
            await self.process.stdin.drain()
        except OSError:
            print(f'Process {self} already closed')

    async def dispatch_process_output(self):
        async for line in self.process.stdout:
            line = line.decode('utf8')
            print('lein', line)
            await self.on_output(line)

class EngineProcessManager(ProcessManager):

    def __init__(self, remote=False):
        super().__init__(ENGINE_PATH, on_output=self.on_engine_message)
        self.create_subscriptions()
        self.engine_running = True
        # threading.Thread(target=self.poll_engine_status, daemon=True).start()

    def create_subscriptions(self):
        pubsub.subscribe(topics.LOAD_ENGINE_GRAMMAR, self.load_engine_grammar)
        pubsub.subscribe(topics.ENGINE_START, self.start)
        pubsub.subscribe(topics.ENGINE_STOP, self.stop)
        # messages.subscribe(messages.LOAD_GRAMMAR, self.load_engine_grammar)
        # messages.subscribe(messages.ENGINE_START, self.start)
        # messages.subscribe(messages.ENGINE_STOP, self.stop)
        # messages.subscribe(messages.STOP_MAIN_PROCESS, self.shutdown)
        pubsub.subscribe(topics.EMULATE_RECOGNITION_EVENT, self.emulate_recognition)
        
    async def send_message(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        await super().send_message(msg)

    async def load_engine_grammar(self, grammar_xml, grammar_id):
        msg = {
            'Type': 'load grammars',
            'Grammar': grammar_xml,
            'Id': grammar_id,
            'StartEngine': self.engine_running
        }
        await self.send_message(msg)

    def poll_engine_status(self):
        while True:
            self.send_simple_message('GET_ENGINE_STATUS')
            time.sleep(5)

    async def on_engine_message(self, msg_string):
        msg = json.loads(msg_string)
        if msg['Type'] == 'recognition':
            if msg['Confidence'] > user_settings['engine']['recognitionConfidence']:
                messages.dispatch(messages.PERFORM_COMMANDS, msg['Commands'], msg['GrammarId'])
        elif msg['Type'] == messages.SET_ENGINE_STATUS:
            messages.dispatch(messages.SET_ENGINE_STATUS, msg)
        elif msg['Type'] == 'error':
            print('error!')
            print(msg['Message'])
        elif msg['Type'] == 'DEBUG':
            print(f'Debug Message:\n{msg["Message"]}')
        elif msg['Type'] == 'RESET_DEVICE':
            await self.send_simple_message(msg['Type'])

    async def send_simple_message(self, msg_type):
        await self.send_message({'Type': msg_type})

    async def shutdown(self):
        await self.send_simple_message('shutdown')

    async def stop(self):
        self.engine_running = False
        await self.send_simple_message('stop')

    async def start(self):
        self.engine_running = True
        await self.send_simple_message('start')

    async def emulate_recognition(self, text, delay=5):
        msg = {
            'Type': 'emulate recognition',
            'Delay': delay,
            'Text': text
        }
        await asyncio.sleep(delay)
        await self.send_message(msg)
