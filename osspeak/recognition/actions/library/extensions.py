import os
import queue
import threading
import importlib.util

import settings

imported_modules = {}

def run(path, alias=None):
    runpath = get_runpath(path)
    save_as = path if alias is None else alias
    imported_modules[save_as] = load_module(runpath)

def send_message(path, msg):
    runpath = get_runpath(path)
    imported_modules[path].module.osspeak_queue.put(msg)

def get_runpath(path):
    if path.endswith('.py'):
        path = path[:-3]
    filepath = path.replace('.', os.sep) + '.py'
    return os.path.join(settings.settings['command_directory'], filepath)

def call(path, function, *args):
    module = imported_modules[path]
    getattr(module, function)(*args)

def close(path):
    imported_modules[path].shutdown_message_queue.put(None)

def load_module(path):
    # prepare to load module from path
    spec = importlib.util.spec_from_file_location('main', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module