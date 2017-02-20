from log import logger
import queue
import threading
import collections

ENGINE_STOP = 'engine stop'
HEARTBEAT = 'heartbeat'
EMULATE_RECOGNITION = 'emulate recognition'
START_ENGINE_LISTENING = 'start engine listening'
SHUTDOWN = 'shutdown'
SET_SAVED_MODULES = 'set saved modules'
PERFORM_COMMANDS = 'perform commands'
LOAD_MODULE_MAP = 'load module map'
RELOAD_COMMAND_MODULE_FILES = 'reload command module files'


_subscriptions = collections.defaultdict(list)

def dispatch(message_name, *args, **kwargs):
    logger.debug(f"Dispatching message: '{message_name}'")
    for sub in _subscriptions[message_name]:
        sub.payload_queue.put((args, kwargs))

def dispatch_sync(message_name, *args, **kwargs):
    logger.debug(f"Dispatching sync message: '{message_name}'")
    for sub in _subscriptions[message_name]:
        sub.callback(*args, **kwargs)

def subscribe(message_name, callback):
    sub = Subscription(callback, message_name)
    _subscriptions[message_name].append(sub)
    return sub

def unsubscribe(subscription):
    if subscription.name in _subscriptions:
        _subscriptions[subscription.name] = [s for s in _subscriptions[subscription.name] if s is not subscription]

class Subscription:

    def __init__(self, callback, name):
        self.callback = callback
        self.name = name
        self.payload_queue = queue.Queue()
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while True:
            args, kwargs = self.payload_queue.get()
            self.callback(*args, **kwargs)
