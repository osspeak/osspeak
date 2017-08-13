import subprocess
import sys
import threading
import json
import os
from communication.procs import ProcessManager
from communication import messages, common
from interfaces.gui import serializer, server
from flask import Flask

if getattr(sys, 'frozen', False):
    ELECTRON_PATH = os.path.join('f')
else:
    ELECTRON_PATH = os.path.join('..', 'gui', 'node_modules', 'electron', 'dist', 'electron.exe')

ELECTRON_FOLDER = os.path.join(' ..', 'gui')

class GuiProcessManager(ProcessManager):

    def __init__(self):
        self.port = common.get_open_port()
        super().__init__(f'{ELECTRON_PATH} {ELECTRON_FOLDER} http://localhost:{self.port}')

    @property
    def command_line_args(self):
        args = {
            'address': f'localhost:{self.port}'
        }
        return json.dumps(args)

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
    
    def main_loop(self):
        server.app.run(port=self.port, host='localhost', threaded=True)