import asyncio
import sys

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

import argparse
import log
import clargs
from recognition.commands import monitor
from communication import server, client, pubsub, topics
from user import settings
from interfaces import create_ui_manager
from engine.handler import EngineProcessHandler
from engine.client import RemoteEngineClient
import threading
import atexit

def main():
    args = clargs.get_args()
    engine = asyncio.get_event_loop().run_until_complete(initialize_speech_engine_connector())
    if settings.user_settings['network'] != 'server':
        ui_manager = create_ui_manager()
        monitor.start_watching_user_state()
        threading.Thread(target=ui_manager.start, daemon=True).start()
    server.run_communication_server()

@atexit.register
def shutdown():
    pubsub.publish(topics.STOP_MAIN_PROCESS)
    for task in asyncio.Task.all_tasks():
        task.cancel()

async def initialize_speech_engine_connector():
    network = settings.user_settings['network']
    if network == 'remote':
        engine_client = client.RemoteEngineClient()
        return engine_client
    else:
        is_server = network == 'server'
        return await EngineProcessHandler.create(remote=is_server)

if __name__ == "__main__":
    main()
