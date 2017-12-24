import websockets
import asyncio
import json
from communication import procs, messages, common
from engine.server import RemoteEngineServer
from settings import settings, get_server_address
from log import logger
from aiohttp import web

loop = asyncio.get_event_loop()

def run_communication_server():
    server_handlers = []
    if settings['network'] == 'server':
        host, port = common.get_host_and_port(settings['server_address'])
        handler = RemoteEngineServer().websocket_handler
        server_handlers.append((handler, host, port))
    for handler, host, port in server_handlers:
        ws_future = websockets.serve(handler, host, port)
        asyncio.get_event_loop().run_until_complete(ws_future)
    asyncio.get_event_loop().run_forever()

def shutdown(l):
    l.stop()