import json
import xml.etree.ElementTree as ET
import asyncio
import sys
from settings import settings
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
        
    async def message_engine(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        await self.process.send_message(msg)

    async def load_engine_grammar(self, grammar_xml, grammar_id):
        msg = {
            'Type': topics.LOAD_ENGINE_GRAMMAR,
            'Grammar': grammar_xml,
            'Id': grammar_id,
            'StartEngine': self.engine_running
        }
        await self.message_engine(msg)

    def poll_engine_status(self):
        while True:
            self.send_simple_message('GET_ENGINE_STATUS')
            time.sleep(5)

    async def dispatch_engine_message(self, topic, *a, **kw):
        if self.server is None:
            pubsub.publish(topic, *a, **kw)
        else:
            await self.server.send_message(topic, *a, **kw)

    async def on_engine_message(self, msg_string):
        msg = json.loads(msg_string)
        if msg['Type'] == 'recognition':
            if msg['Confidence'] > settings['engine']['recognitionConfidence']:
                await self.dispatch_engine_message(topics.PERFORM_COMMANDS, msg['GrammarId'], msg['Words'])
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
        await self.message_engine({'Type': msg_type})

    def shutdown(self):
        if self.process is not None:
            self.process.kill()

    async def stop(self):
        await self.send_simple_message(topics.ENGINE_STOP)
        self.engine_running = False

    async def start(self):
        await self.send_simple_message(topics.ENGINE_START)
        self.engine_running = True

    async def emulate_recognition(self, text, delay=5):
        msg = {
            'Type': topics.EMULATE_RECOGNITION_EVENT,
            'Delay': delay,
            'Text': text
        }
        await asyncio.sleep(5)
        await self.message_engine(msg)