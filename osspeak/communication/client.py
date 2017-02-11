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
        self.socket.setblocking(1)
        self.shutdown_event = threading.Event()
        messages.subscribe('heartbeat', lambda: self.shutdown_event.set())
        message_subscriptions = ('start engine listening', 'engine stop', 'shutdown', 'emulate recognition', 'hearbeat')
        for message in message_subscriptions:
            cb = functools.partial(common.send_message, self.socket, message)
            messages.subscribe(message, cb) 

    def connect(self):
        from user.settings import user_settings
        from log import logger
        host, port = user_settings['server_address']['host'], user_settings['server_address']['port']
        logger.debug(f'Connecting to engine server at {host}:{port}')
        try:
            self.socket.connect((host, int(port)))
            threading.Thread(target=common.receive_loop, daemon=True, args=(self.socket,)).start()
        except OSError:
            logger.warning(f'Unable to connect to {host}:{port}')

    def heartbeat(self):
        while not self.shutdown_event.is_set():
            messages.dispatch('heartbeat')
            self.shutdown_event.wait(timeout=1)

