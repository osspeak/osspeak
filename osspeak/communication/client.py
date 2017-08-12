import asyncio
import requests
import functools
import threading
import json
import socket
import time
import sys
import queue
from log import logger
import user.settings
from user.settings import user_settings
from communication import messages, common

class RemoteEngineClient:

    def __init__(self):
        self.server_address = user.settings.get_server_address()
        self.poll_request_count = 0
        messages.subscribe(messages.SET_ENGINE_STATUS, self.set_engine_status)
        message_subscriptions = (
            messages.LOAD_GRAMMAR,
            messages.ENGINE_STOP,
            messages.EMULATE_RECOGNITION,
            messages.HEARTBEAT,
        )
        for message in message_subscriptions:
            cb = functools.partial(self.send_or_queue_message, message)
            messages.subscribe(message, cb)

    def set_engine_status(self, status_message):
        self.send_poll_request()

    def send_poll_request(self):
        if self.poll_request_count >= 5:
            return
        self.poll_request_count += 1
        url = f'{self.server_address}/poll'
        try:
            resp = requests.get(url, timeout=360)
        except requests.exceptions.RequestException:
            self.poll_request_count -= 1
        else:
            self.poll_request_count -= 1
            common.receive_message(resp.data)
            self.send_poll_request()

    def send_or_queue_message(self, message_name, *args, **kwargs):
        msg = {'name': message_name, 'args': args, 'kwargs': kwargs}
        url = f'{self.server_address}/message'
        try:
            requests.post(url, json=msg)
        except requests.exceptions.RequestException:
            logger.warning('Message send error')