import json
import aiohttp
from communication.server import app
from communication.common import publish_json_message

class RemoteEngineServer:
    
    def __init__(self):
        self.ws = None
        app.add_get('/engine/ws', self.websocket_handler)

    async def websocket_handler(request):
        if self.ws is not None:
            print('already have a connection')
            return
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(request)

        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                publish_json_message(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                        ws.exception())

        print('websocket connection closed')
        self.ws = None

    async def send_message(self, topic, content):
        if not isinstance(msg, str):
            msg = msg.dumps(msg)
        await self.ws.send_str(msg)
    