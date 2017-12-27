import sys
import os

from communication.procs import ProcessHandler
if getattr(sys, 'frozen', False):
    ELECTRON_PATH = os.path.join('f')
else:
    ELECTRON_PATH = os.path.join('..', 'gui', 'node_modules', 'electron', 'dist', 'electron.exe')


async def start_electron():
    proc = await ProcessHandler.create(ELECTRON_PATH, on_output=foo)
    
async def foo(a):
    print(a)