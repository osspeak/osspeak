import subprocess
import sys
import threading
import json
from aiohttp import web
import aiohttp
from communication.procs import ProcessManager

if getattr(sys, 'frozen', False):
    ELECTRON_PATH = r'engines\wsr\RecognizerIO.exe'
else:
    ELECTRON_PATH = '..\\gui\\node_modules\\electron\\dist\\electron.exe ..\\gui\\'

class GuiProcessManager(ProcessManager):

    def __init__(self, event_dispatcher):
        super().__init__(ELECTRON_PATH)
        self.event_dispatcher = event_dispatcher
        self.websocket_established = False
        self.message_queue = []
        self.on_message = {
            'save modules': self.save_modules
        }

    def save_modules(self, msg_data):
        self.event_dispatcher.cmd_module_watcher.modules_to_save = msg_data['modules']

    async def hello(self, request):
        return web.Response(text="Hello, world")
    
    def start_server(self):
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
        print('websocket connection closed')
        return self.ws

    def send_message(self, name, payload=None, encoder=None):
        payload = payload or {}
        msg = json.dumps({'type': name, 'payload': payload}, cls=encoder)
        if not self.websocket_established:
            with threading.Lock():
                self.message_queue.append(msg)
        else:
            self.ws.send_str(msg)