import functools
import threading
import json
import socket
import time
import sys
from communication import messages, common

HOST, PORT = "localhost", 8888

data = 'foobar'


class RemoteEngineClient:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message_subscriptions = ('start engine listening', 'engine stop', 'shutdown', 'emulate recognition')
        for message in message_subscriptions:
            cb = functools.partial(common.send_message, self.socket, message)
            messages.subscribe(message, cb) 

    def connect(self):
    # Create a socket (SOCK_STREAM means a TCP socket)
        # Connect to server and send data
        self.socket.connect((HOST, PORT))
        threading.Thread(target=common.receive_loop, daemon=True, args=(self.socket,)).start()

