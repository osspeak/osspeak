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

def subscribe(message_name, callback):
    sub = Subscription(callback)
    _subscriptions[message_name].append(sub)

class Subscription:

    def __init__(self, callback):
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.callback = callback
        self.payload_queue = queue.Queue()
        self.thread.start()

    def run(self):
        while True:
            args, kwargs = self.payload_queue.get()
            self.callback(*args, **kwargs)
