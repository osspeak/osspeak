import json
import queue
import functools
import asyncio
from communication import pubsub, topics
from communication.common import publish_json_message, yield_queue_contents, put_message_in_queue, receive_ws_messages
import settings

class RemoteEngineClient:

    def __init__(self):
        self.url = f'ws://{settings.settings["server_address"]}'
        self.ws = None
        self.queue = queue.Queue(maxsize=5)
        self.create_subscriptions()
        asyncio.ensure_future(self.connection_loop())

    def create_subscriptions(self):
        from communication.server import loop
        sub_topics = (
            topics.LOAD_ENGINE_GRAMMAR,
            topics.ENGINE_START,
            topics.ENGINE_STOP,
            topics.EMULATE_RECOGNITION_EVENT,
        )
        for sub_topic in sub_topics:
            cb = lambda *a, **kw: asyncio.ensure_future(self.publish_message_to_server(sub_topic, *a, **kw), loop=loop)
            pubsub.subscribe(sub_topic, cb)

    async def connection_loop(self):
        import websockets
        while True:
            try:
                async with websockets.connect(self.url) as self.ws:                  
                    print('got the connect')
                    await receive_ws_messages(self.ws)
                self.ws = None
            except ConnectionRefusedError:
                await asyncio.sleep(30)

    async def publish_message_to_server(self, topic, *args, **kwargs):
        msg = {
            'topic': topic,
            'args': args,
            'kwargs': kwargs,
        }
        encoded_message = json.dumps(msg)
        if self.ws is None:
            put_message_in_queue(self.queue, encoded_message)
        else:
            await self.ws.send(encoded_message)

    async def send_queued_messages(self):
        for msg in yield_queue_contents(self.queue):
            self.ws.send_str(msg)
