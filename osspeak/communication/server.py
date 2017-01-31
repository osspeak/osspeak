import threading
import socket
import asyncio
import time
import socketserver
import functools
import json
from communication import procs, messages, common

class RemoteEngineServer:

    def __init__(self):
        self.engine = procs.EngineProcessManager()

    def loop_forever(self):
        HOST, PORT = "localhost", 8888

        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
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
        cb = functools.partial(common.send_message, self.request, 'perform commands')
        messages.subscribe('perform commands', cb) 
        threading.Thread(target=common.receive_loop, daemon=True, args=(self.request,)).start()
        while True:
            time.sleep(2)