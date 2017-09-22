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
import tornado.websocket
from tornado import web
import aiohttp
from log import logger
import tornado.ioloop

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
        self.app = web.Application([
            (r'/ws', GuiWebSocket),
        ])
        self.app.listen(self.port)
        super().__init__(f'{ELECTRON_PATH} {ELECTRON_FOLDER} localhost:{self.port}', on_exit=self.shutdown)

    def main_loop(self):
        tornado.ioloop.IOLoop.current().start()

    def shutdown(self):
        tornado.ioloop.IOLoop.current().stop()

class GuiWebSocket(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        messages.subscribe(messages.RECEIVED_GUI_MESSAGE, self.on_message)
        messages.subscribe(messages.SEND_GUI_MESSAGE, self.send_gui_message)
        
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

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(message)
        messages.dispatch(messages.RECEIVED_GUI_MESSAGE, json.loads(message))
    
    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        print(origin)
        return True

    def send_message(self, message_name, msg, msg_id=None, ok=True):
        full_message = {'type': message_name, 'data': msg, 'ok': ok}
        if msg_id is not None:
            full_message['id'] = msg_id
        serialized_message = json.dumps(full_message, default=serializer.GuiEncoder)
        self.write_message(serialized_message)