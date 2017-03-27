import os
import queue
import threading
import importlib.util

import user.settings

extension_threads = {}

def run(path, alias=None):
    runpath = get_runpath(path)
    save_as = path if alias is None else alias
    extension_threads[save_as] = ExtensionThread(runpath)

def send_message(path, msg):
    runpath = get_runpath(path)
    extension_threads[path].module.osspeak_queue.put(msg)

def get_runpath(path):
    if path.endswith('.py'):
        path = path[:-3]
    filepath = path.replace('.', os.sep) + '.py'
    return os.path.join(user.settings.COMMAND_DIRECTORY, filepath)

def call(path, function, *args):
    runpath = get_runpath(path)
    module = extension_threads[path].module
    getattr(module, function)(*args)

class ExtensionThread:

    def __init__(self, runpath):
        self.runpath = runpath
        self.shutdown_message_queue = queue.Queue()
        # prepare to load module from paths
        self.spec = importlib.util.spec_from_file_location('main', runpath)
        self.module = importlib.util.module_from_spec(self.spec)
        self.module.osspeak_queue = queue.Queue()
        self.spec.loader.exec_module(self.module)
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        self.shutdown_message_queue.get()
        del extension_threads[self.runpath]