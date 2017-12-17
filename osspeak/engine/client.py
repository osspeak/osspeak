import aiohttp
import queue
import functools
import asyncio
from communication import pubsub, topics
from communication.common import publish_json_message, yield_queue_contents, put_message_in_queue
from user import settings

class RemoteEngineClient:

    def __init__(self):
        self.url = f'ws://{settings.user_settings["server_address"]}/engine/ws'
        self.ws = None
        self.queue = queue.Queue(maxsize=5)
        self.create_subscriptions()
        asyncio.ensure_future(self.run())

    def create_subscriptions(self):
        sub_topics = (topics.LOAD_ENGINE_GRAMMAR, topics.ENGINE_START, topics.ENGINE_STOP)
        for sub_topic in sub_topics:
            pubsub.subscribe(sub_topic, functools.partial(self.publish_message_to_server, sub_topic))

    async def run(self):
        session = aiohttp.ClientSession()
        while True:
            print('tryna connect at ' + self.url)
            try:
                async with session.ws_connect(self.url) as self.ws:
                    print('yayaya')
                    await self.send_queued_messages()
                    async for msg in self.ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            publish_json_message(msg.data)
                        elif msg.type == aiohttp.WSMsgType.CLOSED:
                            break
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break
            except aiohttp.client_exceptions.ClientConnectorError:
                pass
            self.ws = None
            await asyncio.sleep(30)

    async def publish_message_to_server(self, topic, *args, **kwargs):
        msg = {
            'topic': topic,
            'args': args,
            'kwargs': kwargs,
        }
        encoded_message = json.dumps(msg)
        if self.ws is None:
            print('kaboom')
            put_message_in_queue(encoded_message)
        else:
            await self.ws.send_str(encoded_message)

    async def send_queued_messages(self):
        for msg in yield_queue_contents(self.queue):
            self.ws.send_str(msg)
