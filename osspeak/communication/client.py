import asyncio
import functools
import threading
import json
import socket
import aiohttp
import time
import sys
from log import logger
from user.settings import user_settings
from communication import messages, common

class RemoteEngineClient:

    def __init__(self):
        self.server_address = user_settings['server_address']
        messages.subscribe(messages.STOP_MAIN_PROCESS, lambda: None)
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

    def dispatch_message(self, message_name, *args, **kwargs):
        common.send_message(self.ws, message_name, args, kwargs)

    def establish_websocket_connection(self):
        event_loop = asyncio.get_event_loop()
        threading.Thread(target=self.loop_in_thread, args=(event_loop,), daemon=True).start()
        messages.subscribe(messages.STOP_MAIN_PROCESS, lambda: None)

    async def run_websocket_client(self):
        print('assad')
        async with aiohttp.ClientSession() as session:
            address = 'http://' + self.server_address
            while True:
                try:
                    self.ws = await session.ws_connect(address)
                except aiohttp.client_exceptions.ClientOSError:
                    logger.debug(f'Could not connect to {address}, trying again in 5 seconds')
                    time.sleep(5)
                else:
                    break
            while True:
                print('fsdsf')
                async for msg in self.ws:
                    print(msg, msg.data)
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        common.receive_message(msg)
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break

    def loop_in_thread(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run_websocket_client())

    async def receive_websocket_messages(self):
        async for msg in self.ws:
            print(msg, msg.data)
            if msg.type == aiohttp.WSMsgType.TEXT:
                common.receive_message(msg)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

