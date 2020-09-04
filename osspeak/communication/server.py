import asyncio
import json
from communication import procs, common
from engine.server import RemoteEngineServer
from settings import settings, get_server_address
from log import logger

loop = asyncio.get_event_loop()

def shutdown(l):
    l.stop()