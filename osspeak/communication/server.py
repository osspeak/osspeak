import datetime
import threading
import socket
import asyncio
import time
import socketserver
import functools
import json
from aiohttp import web
from communication import procs, messages, common
from user.settings import user_settings
from log import logger

class RemoteEngineServer:

    def __init__(self):
        self.engine = procs.EngineProcessManager()
        self.app = web.Application()
        self.app.router.add_get('/', hello)
        self.app.router.add_get('/ws', self.websocket_handler)

    def loop_forever(self):
        address = user_settings['server_address'].split(':')
        host, port = (address[0], 8080) if len(address) == 1 else address
        logger.debug(f'Hosting engine server at {host}:{port}')
        print(host, port)
        web.run_app(self.app, host=host, port=int(port))
        
    async def websocket_handler(self, request):
        self.ws = web.WebSocketResponse()
        cb = functools.partial(common.send_message, self.ws, messages.PERFORM_COMMANDS)
        sub = messages.subscribe(messages.PERFORM_COMMANDS, cb) 
        await self.ws.prepare(request)
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                common.receive_message(msg)
            elif msg.type == aiohttp.self.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    self.ws.exception())
        messages.unsubscribe(sub)
        print('websocket connection closed')
        return self.ws

    def shutdown(self):
        messages.dispatch_sync(messages.STOP_MAIN_PROCESS)

class RemoteEngineTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.request.settimeout(20)
        logger.info(f'Connection established with {self.request.getpeername()}')
        cb = functools.partial(common.send_message, self.request, messages.PERFORM_COMMANDS)
        sub = messages.subscribe(messages.PERFORM_COMMANDS, cb) 
        self.receive_loop()
        messages.unsubscribe(sub)
        messages.dispatch(messages.ENGINE_STOP)

    def receive_loop(self):
        leftover = ''
        while True:
            try:
                msg = self.request.recv(1024)
            except socket.timeout as e:
                logger.info(f'Connection closed with {self.request.getpeername()}')
                return
            if msg:
                leftover = common.receive_message(leftover, msg)
            else:
                logger.info(f'Connection closed with {self.request.getpeername()}')
                return

async def hello(request):
    return web.Response(text="Hello, world")
