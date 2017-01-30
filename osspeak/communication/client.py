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

    def loop_forever(self):
    # Create a socket (SOCK_STREAM means a TCP socket)
        # Connect to server and send data
        self.socket.connect((HOST, PORT))
        threading.Thread(target=self.listen, daemon=True).start()
        while True:
            time.sleep(2)
        self.socket.close()

    def listen(self):
        while True:
            received = str(self.socket.recv(65536), "utf-8")
            if received:
                self.on_message_received(received)

    def on_message_received(self, msg):
        json_message = json.loads(msg)
        messages.dispatch(json_message['name'], *json_message['args'], **json_message['kwargs'])

