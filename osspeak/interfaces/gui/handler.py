import json
import asyncio
import sys
from settings import settings
from communication import pubsub, topics
from communication.procs import ProcessHandler
from engine import server

if getattr(sys, 'frozen', False):
    ELECTRON_PATH = os.path.join('f')
else:
    ELECTRON_PATH = os.path.join('..', 'gui', 'node_modules', 'electron', 'dist', 'electron.exe')

class ElectronProcessHandler:

    def __init__(self, remote=False):
        self.process = None
        self.create_subscriptions()
        self.server = server.RemoteEngineServer() if remote else None

    @classmethod
    async def create(cls, *a, **kw):
        instance = cls(*a, **kw)
        instance.process = await ProcessHandler.create(ELECTRON_PATH, on_output=instance.on_engine_message)
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
            'Type': topics.LOAD_ENGINE_GRAMMAR,
            'Grammar': grammar_xml,
            'Id': grammar_id,
            'StartEngine': self.engine_running
        }
        await self.send_message(msg)

    def poll_engine_status(self):
        while True:
            self.send_simple_message('GET_ENGINE_STATUS')
            time.sleep(5)

    async def send_simple_message(self, msg_type):
        await self.send_message({'Type': msg_type})

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
        await self.send_message(msg)