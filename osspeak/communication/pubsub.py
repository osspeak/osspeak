from communication.common import parametrized
import asyncio
import functools
import inspect
import collections

_subscriptions = {}


def subscribe(*a):
    if len(a) == 1:
        def real_decorator(function, *stuff):
            Subscription(a[0], function)
            def wrapper(*args, **kwargs):
                function(*args, **kwargs)
            return wrapper
        return real_decorator
    assert len(a) == 2
    return Subscription(*a)
    
def publish(topic, *args, **kwargs):
    from communication.server import loop
    tasks = []
    for sub in _subscriptions.get(topic, []):
        task = asyncio.ensure_future(sub.callback(*args), loop=loop)
        tasks.append(task)
    return tasks

class Subscription:

    def __init__(self, name, callback):
        self.name = name
        self.callback = callback
        if self.name not in _subscriptions:
            _subscriptions[self.name] = []
        _subscriptions[self.name].append(self)