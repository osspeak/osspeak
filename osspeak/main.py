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

def main():
    args = clargs.get_args()
    if settings.user_settings['network'] == 'server':
        server.RemoteEngineServer().loop_forever()
        return
    ui_manager = create_ui_manager()
    engine = initialize_speech_engine_client()
    try:
        # cmw = cmwatcher.CommandModuleWatcher()
        # cmw.initialize_modules()
        monitor.start_watching_user_state()
        # ui_manager.main_loop()
        threading.Thread(target=ui_manager.main_loop, daemon=True).start()
        # server.run_communication_server()
        while True:
            pass
    finally:
        messages.dispatch_sync(messages.STOP_MAIN_PROCESS)

def initialize_speech_engine_client():
    if settings.user_settings['network'] == 'remote':
        engine_client = client.RemoteEngineClient()
        return engine_client
    else:
        return EngineProcessManager()

if __name__ == "__main__":
    main()
