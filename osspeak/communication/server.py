import datetime
import threading
import socket
import asyncio
import time
import socketserver
import functools
import json
import queue
# import flask
# from flask import Response, jsonify, request
from communication import procs, messages, common
from user.settings import user_settings, get_server_address
from log import logger

# app = flask.Flask(__name__)
# push_message_queue = queue.Queue(maxsize=5)

# @app.route('/status')
# def check_status():
#     return ''

# @app.route('/poll')
# def client_poll():
#     while True:
#         msg = push_message_queue.get()
#         then = msg.pop('timestamp')
#         print(time.clock() - then)
#         return jsonify(msg)

# @app.route('/message', methods=['post'])
# def client_message():
#     common.receive_message(request.data)
#     return ''

# def send_message(self, msg):
#     while True:
#         try:
#             push_message_queue.put_nowait(msg)
#         except queue.Full:
#             try:
#                 push_message_queue.get_nowait()
#             except queue.Empty:
#                 pass
#         else:
#             msg['timestamp'] = time.clock()
#             return

# class RemoteEngineServer:

#     def __init__(self):
#         messages.subscribe(messages.PERFORM_COMMANDS, send_message) 
#         self.engine = procs.EngineProcessManager()

#     def loop_forever(self):
#         host, port = get_server_address()
#         logger.debug(f'Hosting engine server at {host}:{port}')
#         app.run(host=host, port=port, threaded=True)
        
#     def shutdown(self, *a, **k):
#         messages.dispatch_sync(messages.STOP_MAIN_PROCESS)