import sys
import os
import json
from communication import pubsub, topics, server

from communication.procs import ProcessHandler
if getattr(sys, 'frozen', False):
    ELECTRON_PATH = os.path.join('f')
    APP_PATH = os.path.join('..', 'gui')
else:
    ELECTRON_PATH = os.path.join('..', 'gui', 'node_modules', 'electron', 'dist', 'electron.exe')
    APP_PATH = os.path.join('..', 'gui')

async def close():
    server.loop.stop()
    sys.exit()

async def start_electron():
    with open(os.path.join('recognition', 'command-module-schema.json')) as f:
        json_module_schema = f.read()
    args = {'osSep': os.sep, 'jsonModuleSchema': json_module_schema}
    proc = await ProcessHandler.create(ELECTRON_PATH, APP_PATH, json.dumps(args), on_output=foo, on_exit=close)
    
async def foo(a):
    print(a)