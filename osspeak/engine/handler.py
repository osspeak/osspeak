import json
import asyncio
import sys
from user.settings import user_settings
from communication import pubsub, topics, messages
from communication.procs import ProcessHandler
from engine import server

if getattr(sys, 'frozen', False):
    ENGINE_PATH = r'engines\wsr\RecognizerIO.exe'
else:
    ENGINE_PATH = r'..\engines\RecognizerIO\RecognizerIO\bin\Debug\RecognizerIO.exe'

class EngineProcessHandler:

    def __init__(self, remote=False):
        self.process = None
        self.create_subscriptions()
        self.engine_running = True
        self.server = server.RemoteEngineServer() if remote else None

    @classmethod
    async def create(cls, *a, **kw):
        instance = cls(*a, **kw)
        instance.process = await ProcessHandler.create(ENGINE_PATH, on_output=instance.on_engine_message)
        return instance

    def create_subscriptions(self):
        pubsub.subscribe(topics.LOAD_ENGINE_GRAMMAR, self.load_engine_grammar)
        pubsub.subscribe(topics.ENGINE_START, self.start)
        pubsub.subscribe(topics.ENGINE_STOP, self.stop)
        pubsub.subscribe(topics.STOP_MAIN_PROCESS, self.shutdown)
        pubsub.subscribe(topics.EMULATE_RECOGNITION_EVENT, self.emulate_recognition)
        
    async def send_message(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        await self.process.send_message(msg)

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
                pubsub.publish(topics.PERFORM_COMMANDS, msg['Commands'], msg['GrammarId'])
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

    def shutdown(self):
        self.process.kill()

    async def stop(self):
        await self.send_simple_message('stop')
        self.engine_running = False

    async def start(self):
        await self.send_simple_message('start')
        self.engine_running = True

    async def emulate_recognition(self, text, delay=5):
        msg = {
            'Type': 'emulate recognition',
            'Delay': delay,
            'Text': text
        }
        await asyncio.sleep(delay)
        await self.send_message(msg)