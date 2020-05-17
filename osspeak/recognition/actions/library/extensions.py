import os
import queue
import threading
import importlib.util

import settings

imported_modules = {}

def register(path, name):
    from recognition.actions.library import stdlib
    mod = get_or_load_module(path)
    stdlib.namespace[name] = mod

def run(path, alias=None):
    runpath = get_runpath(path)
    save_as = path if alias is None else alias
    mod = load_module(runpath)
    imported_modules[save_as] = mod
    return mod

def get_runpath(path):
    if path.endswith('.py'):
        path = path[:-3]
    filepath = path.replace('.', os.sep) + '.py'
    return os.path.join(settings.settings['command_directory'], filepath)

def get_or_load_module(path):
    try:
        return imported_modules[path]
    except KeyError:
        return run(path)

def call(path, function, *args, **kwargs):
    module = get_or_load_module(path)
    return getattr(module, function)(*args, **kwargs)

def load_module(path):
    # prepare to load module from path
    spec = importlib.util.spec_from_file_location('main', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module