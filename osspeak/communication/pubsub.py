import asyncio
import inspect

_subscriptions = {}

def subscribe(topic: str, callback):
    if topic not in _subscriptions:
        _subscriptions[topic] = []
    sub = Subscription(topic, callback)
    _subscriptions[topic].append(sub)
    return sub
    
def publish(topic, *args, **kwargs):
    from communication.server import loop
    tasks = []
    for sub in _subscriptions.get(topic, []):
        res = sub.callback(*args, **kwargs)
        if inspect.iscoroutinefunction(sub.callback):
            task = asyncio.ensure_future(res, loop=loop)
            tasks.append(task)
        # else:
        #     print(type(res))
        #     print(type(sub.callback))
        #     task = asyncio.ensure_future(res, loop=loop)
        #     tasks.append(task)
    return tasks

async def publish_async(topic, *args, **kwargs):
    from communication.server import loop
    futures = []
    for sub in _subscriptions.get(topic, []):
        future = sub.callback(*args, **kwargs)
        if inspect.iscoroutinefunction(sub.callback):
            futures.append(future)
    return await asyncio.gather(*futures)

class Subscription:

    def __init__(self, topic: str, callback):
        self.topic = topic
        self.callback = callback

def wtf():
    print('wtf')