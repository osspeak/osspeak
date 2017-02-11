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
        messages.dispatch_sync('shutdown')

class RemoteEngineTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.request.settimeout(20)
        logger.info(f'Connection established with {self.request.getpeername()}')
        cb = functools.partial(common.send_message, self.request, 'perform commands')
        sub = messages.subscribe('perform commands', cb) 
        self.receive_loop()
        messages.unsubscribe(sub)
        messages.dispatch('engine stop')

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
                last_message_received = time.clock()
            else:
                logger.info(f'Connection closed with {self.request.getpeername()}')
                return