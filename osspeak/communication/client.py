import asyncio
import requests
import functools
import threading
import json
import socket
# import aiohttp
import time
import sys
import queue
from log import logger
import user.settings
from user.settings import user_settings
from communication import messages, common

class RemoteEngineClient:

    def __init__(self):
        self.server_address = user.settings.get_server_address()
        self.engine_should_be_running = False
        self.engine_connection_established = False
        messages.subscribe(messages.ENGINE_CONNECTION_OK, self.on_engine_connection)
        messages.subscribe(messages.POLL_ENGINE_SERVER, self.poll)
        message_subscriptions = (
            messages.LOAD_GRAMMAR,
            messages.ENGINE_STOP,
            messages.EMULATE_RECOGNITION,
            messages.HEARTBEAT,
        )
        for message in message_subscriptions:
            cb = functools.partial(self.send_or_queue_message, message)
            messages.subscribe(message, cb)
        threading.Thread(target=self.engine_status, daemon=True).start()

    def set_engine_connection(self, value):
        self.engine_connection_established = value

    def on_engine_connection(self):
        if not self.engine_connection_established:
            if self.engine_should_be_running:
                messages.dispatch(messages.RELOAD_GRAMMAR)
            messages.dispatch(messages.POLL_ENGINE_SERVER)
        self.engine_connection_established = True

    def load_grammar(self):
        pass

    def poll(self):
        url = f'{self.server_address}/poll'
        while self.engine_connection_established:
            try:
                resp = requests.get(url, timeout=360)
            except requests.exceptions.RequestException:
                continue
            else:
                common.receive_message(resp.data)

    def engine_status(self):
        url = f'{self.server_address}/status'
        while True:
            now = time.clock()
            try:
                resp = requests.get(url, timeout=10)
                if resp.ok:
                    messages.dispatch(messages.ENGINE_CONNECTION_OK)
                    self.engine_connection_established = True
            except requests.exceptions.RequestException:
                messages.dispatch(messages.ENGINE_CONNECTION_BROKEN)
                self.engine_connection_established = False
            time.sleep(max(now - 10, 0))

    def send_or_queue_message(self, message_name, *args, **kwargs):
        if message_name in (messages.ENGINE_START, messages.LOAD_GRAMMAR):
            self.engine_should_be_running = True
        elif message_name == messages.ENGINE_STOP:
            self.engine_should_be_running = False
        if self.engine_connection_established:
            msg = {'name': message_name, 'args': args, 'kwargs': kwargs}
            url = f'{self.server_address}/message'
            try:
                requests.post(json=msg)
            except requests.exceptions.RequestException:
                logger.warning('Message send error')

    def establish_engine_connection(self):
        event_loop = asyncio.get_event_loop()
        threading.Thread(target=self.loop_in_thread, args=(event_loop,), daemon=True).start()
        messages.subscribe(messages.STOP_MAIN_PROCESS, lambda: None)

    async def run_websocket_client(self):
        async with aiohttp.ClientSession() as session:
            await self.establish_websocket_connection(session)
            await self.receive_websocket_messages()
            messages.dispatch(messages.WEBSOCKET_CONNECTION_BROKEN)
            messages.dispatch(messages.RELOAD_GRAMMAR)

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

