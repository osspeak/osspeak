from log import logger
import queue
import threading
import collections

_subscriptions = collections.defaultdict(list)

def dispatch(message_name, *args, **kwargs):
    logger.debug(f"Dispatching message: '{message_name}'")
    for sub in _subscriptions[message_name]:
        sub.payload_queue.put((args, kwargs))

def dispatch_sync(message_name, *args, **kwargs):
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