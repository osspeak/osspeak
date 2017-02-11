import datetime
import threading
import socket
import asyncio
import time
import socketserver
import functools
import json
from communication import procs, messages, common
from user.settings import user_settings
from log import logger

class RemoteEngineServer:

    def __init__(self):
        self.engine = procs.EngineProcessManager()

    def loop_forever(self):
        host, port = user_settings['server_address']['host'], user_settings['server_address']['port']
        logger.debug(f'Hosting engine server at {host}:{port}')
        try:
            server = socketserver.TCPServer((host, port), RemoteEngineTCPHandler) 
        except OSError as e:
            logger.error(f'Unable to host at {host}:{port}:\n{e}\nShutting down...')
            self.shutdown()
            return
        server.serve_forever()
        server.server_close()
        self.shutdown()

    def shutdown(self):
        messages.dispatch_sync(messages.SHUTDOWN)

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