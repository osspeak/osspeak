import subprocess
import asyncio
import sys
import threading
import json
import os
from communication.procs import ProcessManager
from communication import messages, common
from interfaces.gui import serializer
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
    'FOO': lambda *a: ('sdfsdfsdf'),
    'GET_COMMAND_MODULES': lambda *a: 55
}

class GuiProcessManager(ProcessManager):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.port = common.get_open_port()
        self.app = aiohttp.web.Application()
        self.app.router.add_get('/ws', self.websocket_handler)
        self.websocket_connections = set()
        messages.subscribe(messages.RECEIVED_GUI_MESSAGE, self.on_message)
        messages.subscribe(messages.SEND_GUI_MESSAGE, self.send_gui_message)
        super().__init__(f'{ELECTRON_PATH} {ELECTRON_FOLDER} localhost:{self.port}', on_exit=self.shutdown)

    def send_gui_message(self, message_name, data=None):
        data = {} if data is None else data
        msg_data, ok = self.gui_resource(message_name, data)
        self.send_message(message_name, msg_data, ok=ok)

    def on_message(self, msg):
        msg_data, ok = self.gui_resource(msg['type'], msg.get('data', {}))
        self.send_message(msg['type'], msg_data, msg_id=msg['id'], ok=ok)

    def gui_resource(self, name, data):
        if name not in routes:
            return f'No resource named {name}', False
        data_func = routes[name]
        ok = True
        try:
            result = data_func(data)
        except Exception as e:
            logger.error(str(e))
            result = str(e)
            ok = False
        return result, ok

    def send_message(self, message_name, msg, msg_id=None, ok=True):
        full_message = {'type': message_name, 'data': msg, 'ok': ok}
        if msg_id is not None:
            full_message['id'] = msg_id
        serialized_message = json.dumps(full_message, default=serializer.GuiEncoder)
        for ws in self.websocket_connections:
            ws.send_str(serialized_message)

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
        aiohttp.web.run_app(self.app, host='localhost', port=self.port)

    def shutdown(self):
        self.loop.call_soon_threadsafe(lambda: self.loop.stop())

    async def websocket_handler(self, request):
        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)
        self.websocket_connections.add(ws)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    messages.dispatch(messages.RECEIVED_GUI_MESSAGE, json.loads(msg.data))
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    ws.exception())
        print('websocket connection closed')
        self.websocket_connections.remove(ws)
        return ws