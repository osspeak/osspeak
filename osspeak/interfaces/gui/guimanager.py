import subprocess
import asyncio
import sys
import threading
import json
import os
from communication.procs import ProcessManager
from communication import messages, common
from interfaces.gui import serializer, server
from flask import Flask
from aiohttp import web
import aiohttp
from log import logger

if getattr(sys, 'frozen', False):
    ELECTRON_PATH = os.path.join('f')
else:
    ELECTRON_PATH = os.path.join('..', 'gui', 'node_modules', 'electron', 'dist', 'electron.exe')

ELECTRON_FOLDER = os.path.join(' ..', 'gui')

routes = {
    'FOO': lambda *a: ('sdfsdfsdf')
}

class GuiProcessManager(ProcessManager):

    def __init__(self):
        self.port = common.get_open_port()
        self.app = aiohttp.web.Application()
        self.app.router.add_get('/ws', self.websocket_handler)
        self.websocket_connections = set()
        messages.subscribe(messages.RECEIVED_WEBSOCKET_MESSAGE, self.on_message)
        messages.subscribe(messages.MESSAGE_GUI, self.send_message)
        super().__init__(f'{ELECTRON_PATH} {ELECTRON_FOLDER} localhost:{self.port}')

    @property
    def command_line_args(self):
        args = {
            'address': f'localhost:{self.port}'
        }
        return json.dumps(args)

    def on_message(self, msg):
        data_func = routes[msg['type']]
        ok = True
        try:
            result = data_func(msg.get('data'))
        except Exception as e:
            logger.error(str(e))
            result = str(e)
            ok = False
        self.send_message('RESPONSE', result, ok=ok)

    def send_message(self, message_name, msg, msg_id=None, ok=True):
        full_message = json.dumps({'type': message_name, 'data': msg, 'ok': ok})
        if msg_id is not None:
            assert message_name == 'RESPONSE'
            full_message['id'] = msg_id
        for ws in self.websocket_connections:
            ws.send_str(msg)

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
    
    def main_loop(self):
        loop = asyncio.get_event_loop()
        messages.subscribe(messages.WEBSOCKET_CONNECTION_BROKEN, self.shutdown)
        threading.Thread(target=self.shutdown, daemon=True, args=(loop,)).start()
        aiohttp.web.run_app(self.app, host='localhost', port=self.port)
        # server.app.run(port=self.port, host='localhost', threaded=True)

    def shutdown(self, loop):
        import time
        time.sleep(60)
        loop.call_soon_threadsafe(lambda: loop.stop())

    async def websocket_handler(self, request):
        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)
        self.websocket_connections.add(ws)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    messages.dispatch(messages.RECEIVED_WEBSOCKET_MESSAGE, json.loads(msg.data))
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    ws.exception())
        print('websocket connection closed')
        self.websocket_connections.remove(ws)
        return ws