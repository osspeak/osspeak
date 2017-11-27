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

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")



def run_communication_server():
    pass