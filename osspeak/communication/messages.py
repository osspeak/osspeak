import queue
import threading
import collections

_subscriptions = collections.defaultdict(list)

def dispatch(message_name, *args, **kwargs):
    for sub in _subscriptions[message_name]:
        sub.payload_queue.put((args, kwargs))

def dispatch_sync(message_name, *args, **kwargs):
    for sub in _subscriptions[message_name]:
        sub.callback(*args, **kwargs)

def subscribe(message_names, callback):
    if isinstance(message_names, str):
        message_names = [message_names]
    for name in message_names:
        sub = Subscription(callback)
        _subscriptions[name].append(sub)

class Subscription:

    def __init__(self, callback):
        self.callback = callback
        self.payload_queue = queue.Queue()
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while True:
            args, kwargs = self.payload_queue.get()
            self.callback(*args, **kwargs)
