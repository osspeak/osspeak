import threading
import socket
import asyncio
import time
import socketserver
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
        threading.Thread(target=self.receive_loop, daemon=True).start()
        self.request.setblocking(1)
        while True:
            time.sleep(2)

    def receive_loop(self):
        while True:
            self.data = self.request.recv(65536).strip()
            if self.data:
                self.handle_message(self.data)
            print('eff')
            time.sleep(1)

    def handle_message(self, msg):
        json_message = json.loads(msg)
        messages.dispatch(json_message['name'], *json_message['args'], **json_message['kwargs'])