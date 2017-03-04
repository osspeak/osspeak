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
        messages.subscribe(messages.STOP_MAIN_PROCESS , lambda: self.shutdown_event.set())
        message_subscriptions = (
            messages.START_ENGINE_LISTENING,
            messages.ENGINE_STOP,
            messages.STOP_MAIN_PROCESS,
            messages.EMULATE_RECOGNITION,
            messages.HEARTBEAT,
        )
        for message in message_subscriptions:
            cb = functools.partial(common.send_message, self.socket, message)
            messages.subscribe(message, cb)
        messages.subscribe(STOP_MAIN_PROCESS, lambda: self.socket.close())

    def connect(self):
        from user.settings import user_settings
        from log import logger
        host, port = user_settings['server_address']['host'], user_settings['server_address']['port']
        logger.debug(f'Connecting to engine server at {host}:{port}')
        try:
            self.socket.connect((host, int(port)))
            threading.Thread(target=common.receive_loop, daemon=True, args=(self.socket,)).start()
            threading.Thread(target=self.heartbeat, daemon=True).start()
        except OSError as e:
            logger.warning(f'Unable to connect to {host}:{port}: \n{e}')

    def heartbeat(self):
        while not self.shutdown_event.is_set():
            messages.dispatch_sync(messages.HEARTBEAT)
            self.shutdown_event.wait(timeout=1)

