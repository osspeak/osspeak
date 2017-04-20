import asyncio
import functools
import threading
import json
import socket
import aiohttp
import time
import sys
from user.settings import user_settings
from communication import messages, common

class RemoteEngineClient:

    def __init__(self):
        self.server_address = user_settings['server_address']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(1)
        messages.subscribe(messages.STOP_MAIN_PROCESS , lambda: None)
        message_subscriptions = (
            messages.START_ENGINE_LISTENING,
            messages.ENGINE_STOP,
            messages.STOP_MAIN_PROCESS,
            messages.EMULATE_RECOGNITION,
            messages.HEARTBEAT,
        )
        for message in message_subscriptions:
            cb = functools.partial(self.dispatch_message, message)
            messages.subscribe(message, cb)

    def dispatch_message(message_name, *args, **kwargs):
        common.send_message(self.ws, message_name, args, kwargs)

    def establish_websocket_connection(self):
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.run_websocket_client())
        messages.subscribe(STOP_MAIN_PROCESS, lambda: None)

    async def run_websocket_client(self):
        session = aiohttp.ClientSession()
        while True:
            try:
                self.ws = await session.ws_connect('http://' + self.server_address)
            except aiohttp.errors.ClientOSError:
                print('err')
                pass
            else:
                break

    def receive_websocket_messages(self):
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                common.send_message(msg)
                if msg.data == 'close cmd':
                    await ws.close()
                    break
                else:
                    ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

