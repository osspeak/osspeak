import datetime
import threading
import socket
import asyncio
import time
import socketserver
import functools
import json
import queue
import flask
from flask import Response, jsonify, request
from communication import procs, messages, common
from user.settings import user_settings, get_server_address
from log import logger

app = flask.Flask(__name__)

class RemoteEngineServer:

    def __init__(self):
        self.push_message_queue = queue.Queue(maxsize=5)
        messages.subscribe(messages.PERFORM_COMMANDS, self.send_message) 
        self.engine = procs.EngineProcessManager()

    @app.route('/status')
    def check_status(self):
        return ''

    @app.route('/poll')
    def client_poll(self):
        while True:
            msg = self.push_message_queue.get()
            then = msg.pop('timestamp')
            print(time.clock() - then)
            return jsonify(msg)

    @app.route('/message', methods=['post'])
    def client_message(self):
        common.receive_message(request.data)
        return ''

    def loop_forever(self):
        host, port = get_server_address()
        logger.debug(f'Hosting engine server at {host}:{port}')
        print('wtf', host, port)
        app.run(host=host, port=port, threaded=True)
        
    def send_message(self, msg):
        while True:
            try:
                self.push_message_queue.put_nowait(msg)
            except queue.Full:
                try:
                    self.push_message_queue.get_nowait()
                except queue.Empty:
                    pass
            else:
                msg['timestamp'] = time.clock()
                return

    def shutdown(self, *a, **k):
        messages.dispatch_sync(messages.STOP_MAIN_PROCESS)