import json
import asyncio
from log import logger
import websockets
import settings
from settings import settings
from communication import common

class RemoteEngineServer:
    
    def __init__(self):
        self.ws = None

    async def websocket_handler(self, websocket, path):
        if self.ws is not None:
            print('already have a connection')
            return
        self.ws = websocket
        while True:
            try:
                msg = await websocket.recv()
            except websockets.exceptions.ConnectionClosed:
                logger.warning('Connection closed')
                break
            else:
                common.publish_json_message(msg)
        self.ws = None

    async def send_message(self, topic, *a, **kw):
        encoded_message = common.topic_message(topic, *a, **kw)
        await self.ws.send(encoded_message)