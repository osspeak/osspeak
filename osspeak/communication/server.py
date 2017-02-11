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
        with socketserver.TCPServer((host, port), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.request.settimeout(1)
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
            except IndexError as e:
                logger.info(f'Connection closed with {self.request.getpeername()}')
                return
            if msg:
                leftover = common.receive_message(leftover, msg)
                last_message_received = time.clock()
            else:
                logger.info(f'Connection closed with {self.request.getpeername()}')
                return