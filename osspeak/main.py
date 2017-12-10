import argparse
import asyncio

import log
import clargs
from recognition.commands import monitor
from communication import server, client, messages
from user import settings
from interfaces import create_ui_manager
from client import cmwatcher
from communication.procs import EngineProcessManager
import threading
import atexit

def main():
    args = clargs.get_args()
    if settings.user_settings['network'] == 'server':
        server.RemoteEngineServer().loop_forever()
        return
    ui_manager = create_ui_manager()
    engine = initialize_speech_engine_client()
    loop = asyncio.get_event_loop()
    try:
        monitor.start_watching_user_state()
        threading.Thread(target=ui_manager.start, daemon=True).start()
        server.run_communication_server()
        # while True:
        #     pass
    finally:
        # asyncio.get_event_loop().stop()
        messages.dispatch_sync(messages.STOP_MAIN_PROCESS)

@atexit.register
def shutdown():
    return
    asyncio.get_event_loop().stop()
    # asyncio.get_event_loop().close()

def initialize_speech_engine_client():
    if settings.user_settings['network'] == 'remote':
        engine_client = client.RemoteEngineClient()
        return engine_client
    else:
        return EngineProcessManager()

if __name__ == "__main__":
    main()
