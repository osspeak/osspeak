import json
import asyncio
from log import logger
import websockets
import settings
from settings import settings
from communication.common import publish_json_message, get_host_and_port

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
                publish_json_message(msg)
        self.ws = None

    async def send_message(self, topic, content):
        if not isinstance(msg, str):
            msg = msg.dumps(msg)
        await self.ws.send(msg)