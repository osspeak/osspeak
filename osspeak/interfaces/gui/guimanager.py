import subprocess
import sys
import threading
import json
import os
# from aiohttp import web
# import aiohttp
from communication.procs import ProcessManager
from communication import messages, common
from interfaces.gui import serializer, server
from flask import Flask
# from flask_sockets import Sockets

if getattr(sys, 'frozen', False):
    ELECTRON_PATH = os.path.join('f')
else:
    ELECTRON_PATH = os.path.join('..', 'gui', 'node_modules', 'electron', 'dist', 'electron.exe')

ELECTRON_FOLDER = os.path.join(' ..', 'gui')

class GuiProcessManager(ProcessManager):

    def __init__(self):
        super().__init__(f'{ELECTRON_PATH} {ELECTRON_FOLDER}')
        # messages.subscribe(messages.LOAD_MODULE_MAP, lambda payload: self.send_message('module map', payload))
        # messages.subscribe(messages.WEBSOCKET_CONNECTION_ESTABLISHED, self.on_connected)

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

    def stop(self):
        self.server.stop()

    def on_message(self, msg, ws):
        msg_dict = json.loads(msg.data)
        self.message_dispatcher[msg_dict['type']](msg_dict['payload'])
    
    def main_loop(self):
        port = common.get_open_port()
        server.app.run(port=port)

    def on_connected(self, ws):
        self.open_sockets.add(ws)
        while not ws.closed:
            message = ws.receive()
            messages.dispatch(messages.RECEIVED_WEBSOCKET_MESSAGE, ws, message)
        self.open_sockets.remove(ws)
        self.stop()

    def send_message(self, name, payload=None, encoder=None):
        payload = payload or {}
        msg = json.dumps({'type': name, 'payload': payload}, cls=serializer.GuiEncoder)
        if not self.websocket_established:
            with threading.Lock():
                self.message_queue.append(msg)
        else:
            self.ws.send_str(msg)