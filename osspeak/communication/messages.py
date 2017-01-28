import queue
import threading
import collections

_subscriptions = collections.defaultdict(list)

def dispatch(message_name, payload=None):
    payload = {} if payload is None else payload
    for sub in _subscriptions[message_name]:
        sub.payload_queue.put(payload)

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
            payload = self.payload_queue.get()
            self.callback(payload)
