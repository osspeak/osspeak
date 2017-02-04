import functools
import threading
import json
import socket
import time
import sys
from communication import messages, common

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
        from user.settings import user_settings
        from log import logger
        host, port = user_settings['server_address']['host'], user_settings['server_address']['port']
        logger.debug(f'Connecting to engine server at {host}:{port}')
        try:
            self.socket.connect((host, port))
            threading.Thread(target=common.receive_loop, daemon=True, args=(self.socket,)).start()
        except OSError:
            logger.warning(f'Unable to connect to {host}:{port}')

