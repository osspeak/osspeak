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
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await self.ws.close()
                else:
                    self.send_message('foo')
                    # self.ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    self.ws.exception())
        print('websocket connection closed')
        return self.ws

    def send_message(self, name, payload=None):
        payload = payload or {}
        msg = json.dumps({'type': name, 'payload': payload})
        if not self.websocket_established:
            with threading.Lock():
                self.message_queue.append(msg)
        else:
            self.ws.send_str(msg)