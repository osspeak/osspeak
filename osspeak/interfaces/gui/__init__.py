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
    args = {'osSep': os.sep}
    proc = await ProcessHandler.create(ELECTRON_PATH, APP_PATH, json.dumps(args), on_output=foo, on_exit=close)
    
async def foo(a):
    print(a)