import asyncio
import functools
import threading
import json
import socket
import aiohttp
import time
import sys
import queue
from log import logger
from user.settings import user_settings
from communication import messages, common

class RemoteEngineClient:

    def __init__(self):
        self.server_address = user_settings['server_address']
        self.ws = None
        self.message_queue = []
        self.message_queue_lock = threading.Lock()
        messages.subscribe(messages.WEBSOCKET_CONNECTION_ESTABLISHED, lambda: self.send_all_messages())
        messages.subscribe(messages.STOP_MAIN_PROCESS, lambda: None)
        message_subscriptions = (
            messages.LOAD_GRAMMAR,
            messages.ENGINE_STOP,
            messages.STOP_MAIN_PROCESS,
            messages.EMULATE_RECOGNITION,
            messages.HEARTBEAT,
        )
        for message in message_subscriptions:
            cb = functools.partial(self.send_or_queue_message, message)
            messages.subscribe(message, cb)

    def send_all_messages(self):
        with self.message_queue_lock:
            while self.message_queue:
                try:
                    msg = self.message_queue[-1]
                    common.send_message(self.ws, msg['name'], *msg['args'], **msg['kwargs'])
                except AttributeError:
                    return
                self.message_queue.pop()

    def send_or_queue_message(self, message_name, *args, **kwargs):
        msg = {'name': message_name, 'args': args, 'kwargs': kwargs}
        with self.message_queue_lock:
            # potential queue clearing logic here
            self.message_queue.insert(0, msg)
        self.send_all_messages()

    def start_websocket_loop(self):
        event_loop = asyncio.get_event_loop()
        threading.Thread(target=self.loop_in_thread, args=(event_loop,), daemon=True).start()
        messages.subscribe(messages.STOP_MAIN_PROCESS, lambda: None)

    async def run_websocket_client(self):
        async with aiohttp.ClientSession() as session:
            await self.establish_websocket_connection(session)
            await self.receive_websocket_messages()
            messages.dispatch(messages.WEBSOCKET_CONNECTION_BROKEN)

    async def establish_websocket_connection(self, session):
        address = 'http://' + self.server_address
        while True:
            try:
                self.ws = await session.ws_connect(address)
                messages.dispatch(messages.WEBSOCKET_CONNECTION_ESTABLISHED)
                return
            except aiohttp.client_exceptions.ClientConnectorError:
                logger.debug(f'Could not connect to {address}, trying again in 5 seconds')
                time.sleep(5)

    def loop_in_thread(self, loop):
        asyncio.set_event_loop(loop)
        while True:
            loop.run_until_complete(self.run_websocket_client())

    async def receive_websocket_messages(self):
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                common.receive_message(msg.data)
            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                return

