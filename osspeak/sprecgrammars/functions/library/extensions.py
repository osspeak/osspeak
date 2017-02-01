import os
import queue
import threading
import importlib.util

import user.settings

extension_threads = {}

def run(path):
    runpath = get_runpath(path)
    extension_threads[runpath] = ExtensionThread(runpath)

def send_message(path, msg):
    runpath = get_runpath(path)
    extension_threads[runpath].module.osspeak_queue.put(msg)

def get_runpath(path):
    if path.endswith('.py'):
        path = path[:-3]
    filepath = path.replace('.', os.sep) + '.py'
    return os.path.join(user.settings.COMMAND_DIRECTORY, filepath)

class ExtensionThread:

    def __init__(self, runpath):
        self.runpath = runpath
        # prepare to load module from paths
        self.spec = importlib.util.spec_from_file_location('main', runpath)
        self.module = importlib.util.module_from_spec(self.spec)
        self.module.osspeak_queue = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        self.spec.loader.exec_module(self.module)
        if extension_threads[self.runpath] is self:
            del extension_threads[self.runpath]