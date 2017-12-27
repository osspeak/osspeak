import sys
import os

if getattr(sys, 'frozen', False):
    ELECTRON_PATH = os.path.join('f')
else:
    ELECTRON_PATH = os.path.join('..', 'gui', 'node_modules', 'electron', 'dist', 'electron.exe')