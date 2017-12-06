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
from aiohttp import web
import asyncio

loop = asyncio.get_event_loop()
app = web.Application()

def run_communication_server():
    web.run_app(app, loop=loop, print=False)

def shutdown(l):
    l.stop()