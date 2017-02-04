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
        self.request.setblocking(1)
        logger.info(f'Connection established with {self.request.getpeername()}')
        cb = functools.partial(common.send_message, self.request, 'perform commands')
        messages.subscribe('perform commands', cb) 
        socket_broken = threading.Event()
        threading.Thread(target=common.receive_loop, daemon=True, args=(self.request,),
            kwargs={'socket_broken_event': socket_broken}).start()
        socket_broken.wait()
        logger.info(f'Connection closed with {self.request.getpeername()}')
        messages.dispatch('engine stop')

    def on_error(self):
        self.foo = False