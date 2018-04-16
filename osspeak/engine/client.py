import json
import queue
import functools
import asyncio
from communication import pubsub, topics
from communication.common import publish_json_message, yield_queue_contents, put_message_in_queue, receive_ws_messages
import settings
from communication.server import loop

class RemoteEngineClient:

    def __init__(self):
        self.url = f'ws://{settings.settings["server_address"]}'
        self.ws = None
        self.queue = queue.Queue(maxsize=5)
        self.create_subscriptions()
        asyncio.ensure_future(self.connection_loop())

    def create_subscriptions(self):
        sub_topics = (
            topics.LOAD_ENGINE_GRAMMAR,
            topics.ENGINE_START,
            topics.ENGINE_STOP,
            topics.EMULATE_RECOGNITION_EVENT,
            topics.PERFORM_COMMANDS,
        )
        for sub_topic in sub_topics:
            cb = functools.partial(self.publish, sub_topic)
            pubsub.subscribe(sub_topic, cb)

    async def connection_loop(self):
        import websockets
        while True:
            try:
                async with websockets.connect(self.url) as self.ws:                  
                    await receive_ws_messages(self.ws)
                self.ws = None
            except ConnectionRefusedError:
                await asyncio.sleep(30)

    def publish(self, topic, *args, **kwargs):
        fut = self.publish_message_to_server(topic, *args, **kwargs)
        asyncio.ensure_future(fut, loop=loop)

    async def publish_message_to_server(self, topic, *args, **kwargs):
        import websockets
        msg = {
            'topic': topic,
            'args': args,
            'kwargs': kwargs,
        }
        encoded_message = json.dumps(msg)
        try:
            await self.ws.send(encoded_message)
        except (AttributeError, websockets.exceptions.ConnectionClosed):
            put_message_in_queue(self.queue, encoded_message)

    async def send_queued_messages(self):
        for msg in yield_queue_contents(self.queue):
            self.ws.send_str(msg)
 