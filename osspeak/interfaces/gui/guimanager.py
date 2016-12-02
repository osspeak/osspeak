import subprocess
import sys
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

    async def hello(self, request):
        return web.Response(text="Hello, world")
    
    def start_server(self):
        self.app = web.Application()
        self.app.router.add_get('/', self.hello)
        self.app.router.add_get('/websocket', self.websocket_handler)
        web.run_app(self.app)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            print('msg', msg)
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    ws.exception())
        print('websocket connection closed')
        return ws