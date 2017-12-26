import asyncio
import sys

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

import log
import clargs
from recognition.commands import monitor
from communication import server, pubsub, topics
import settings
from interfaces import create_ui_manager
from engine.handler import EngineProcessHandler
from engine.client import RemoteEngineClient
import threading
import atexit

def main():
    engine = asyncio.get_event_loop().run_until_complete(initialize_speech_engine_connector())
    if settings.settings['network'] != 'server':
        monitor.start_watching_user_state()
    cli_loop = get_cli_loop()
    threading.Thread(target=cli_loop, daemon=True).start()
    server.run_communication_server()

@atexit.register
def shutdown():
    pubsub.publish(topics.STOP_MAIN_PROCESS)
    for task in asyncio.Task.all_tasks():
        task.cancel()

async def initialize_speech_engine_connector():
    network = settings.settings['network']
    if network == 'remote':
        return RemoteEngineClient()
    else:
        is_server = network == 'server'
        return await EngineProcessHandler.create(remote=is_server)

def get_cli_loop():
    no_cli = settings.settings['interface'] == 'gui' or settings.settings['network'] == 'server'
    if no_cli:
        input_blocker = lambda: input('')
    else:
        input_blocker = menu.MainMenu().start

    def loop_func():
        input_blocker()
        server.loop.stop()

    return loop_func


if __name__ == "__main__":
    main()
