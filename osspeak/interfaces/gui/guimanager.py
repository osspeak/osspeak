import subprocess
import sys
import threading
import json
from aiohttp import web
import aiohttp
from communication.procs import ProcessManager
from communication import messages
from interfaces.gui import serializer

if getattr(sys, 'frozen', False):
    ELECTRON_PATH = r'engines\wsr\RecognizerIO.exe'
else:
    ELECTRON_PATH = '..\\gui\\node_modules\\electron\\dist\\electron.exe ..\\gui\\'

class GuiProcessManager(ProcessManager):

    def __init__(self):
        super().__init__(ELECTRON_PATH)
        self.websocket_established = False
        self.message_queue = []
        self.message_queue_lock = threading.Lock()
        self.on_message = {
            'save modules': self.save_modules
        }
        messages.subscribe(messages.LOAD_MODULE_MAP, lambda payload: self.send_message('module map', payload))

    def save_modules(self, msg_data):
        module_configurations = {k: self.to_module_config(v) for (k, v) in msg_data['modules'].items()}
        messages.dispatch(messages.SET_SAVED_MODULES, module_configurations)

    def to_module_config(self, gui_module):
        module_config = {}
        for k, config in gui_module.items():
            if k in ('path', 'error'):
                continue
            elif k == 'functions':
                module_config[k] = [[c['signature']['value'], c['action']['value']] for c in config]
            elif k == 'rules':
                module_config[k] = [[c['name']['value'], c['value']['value']] for c in config]
            elif k == 'commands':
                module_config[k] = [[c['rule']['value']['value'], c['action']['value']] for c in config]
            else:
                module_config[k] = config
        return module_config

    async def hello(self, request):
        return web.Response(text="Hello, world")
    
    def main_loop(self):
        self.app = web.Application()
        self.app.router.add_get('/', self.hello)
        self.app.router.add_get('/websocket', self.websocket_handler)
        web.run_app(self.app)

    async def websocket_handler(self, request):
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(request)
        self.websocket_established = True
        with threading.Lock():
            for msg in self.message_queue:
                self.ws.send_str(msg)
            del self.message_queue[:]
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                msg_dict = json.loads(msg.data)
                self.on_message[msg_dict['type']](msg_dict['payload'])
                if msg.data == 'close':
                    await self.ws.close()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    self.ws.exception())
        messages.dispatch(messages.STOP_MAIN_PROCESS )
        print('websocket connection closed')
        return self.ws

    def send_message(self, name, payload=None, encoder=None):
        payload = payload or {}
        msg = json.dumps({'type': name, 'payload': payload}, cls=serializer.GuiEncoder)
        if not self.websocket_established:
            with threading.Lock():
                self.message_queue.append(msg)
        else:
            self.ws.send_str(msg)