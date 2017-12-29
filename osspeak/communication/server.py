import asyncio
import json
from communication import procs, messages, common
from engine.server import RemoteEngineServer
from interfaces.gui.ws import gui_websocket_handler
from settings import settings, get_server_address
from log import logger

loop = asyncio.get_event_loop()

def get_websocket_handlers():
    websocket_handlers = []
    if settings['network'] == 'server':
        host, port = common.get_host_and_port(settings['server_address'])
        handler = RemoteEngineServer().websocket_handler
        websocket_handlers.append((handler, host, port))
    if settings['interface'] == 'gui':
        websocket_handlers.append((gui_websocket_handler, 'localhost', settings['gui_port']))
    return websocket_handlers
        
async def start_websockets(websocket_handlers):
    import websockets
    futures = []
    for handler, host, port in websocket_handlers:
        ws_future = websockets.serve(handler, host, port)
        futures.append(ws_future)
    await asyncio.gather(*futures)

def shutdown(l):
    l.stop()