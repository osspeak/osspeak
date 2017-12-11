import asyncio
import inspect

_subscriptions = {}

def subscribe(topic, callback):
    return Subscription(topic, callback)
    
def publish(topic, *args, **kwargs):
    from communication.server import loop
    tasks = []
    for sub in _subscriptions.get(topic, []):
        res = sub.callback(*args, **kwargs)
        if inspect.iscoroutinefunction(sub.callback):
            task = asyncio.ensure_future(res, loop=loop)
            tasks.append(task)
    return tasks

class Subscription:

    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback
        if self.topic not in _subscriptions:
            _subscriptions[self.topic] = []
        _subscriptions[self.topic].append(self)