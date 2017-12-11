import asyncio
import sys

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

import argparse
import log
import clargs
from recognition.commands import monitor
from communication import server, client, messages, pubsub, topics
from user import settings
from interfaces import create_ui_manager
from client import cmwatcher
from communication.procs import EngineProcessManager, ENGINE_PATH
import threading
import atexit

def main():
    args = clargs.get_args()
    if settings.user_settings['network'] == 'server':
        server.RemoteEngineServer().loop_forever()
        return
    ui_manager = create_ui_manager()
    engine = asyncio.get_event_loop().run_until_complete(initialize_speech_engine_client())
    try:
        monitor.start_watching_user_state()
        threading.Thread(target=ui_manager.start, daemon=True).start()
        server.run_communication_server()
    finally:
        pubsub.publish(topics.STOP_MAIN_PROCESS)
        asyncio.get_event_loop().close()
        print('finally')

# @atexit.register
# def shutdown():
#     return
#     asyncio.get_event_loop().stop()
    # asyncio.get_event_loop().close()

async def initialize_speech_engine_client():
    if settings.user_settings['network'] == 'remote':
        engine_client = client.RemoteEngineClient()
        return engine_client
    else:
        return await EngineProcessManager.create(ENGINE_PATH)

if __name__ == "__main__":
    main()
