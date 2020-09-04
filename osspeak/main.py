import asyncio
import sys

import settings
if __name__ == "__main__":
    user_settings = settings.load_user_settings()
    settings.set_settings(user_settings)

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

from communication import server, pubsub, topics
from interfaces.cli import menu
from engine.handler import EngineProcessHandler
from engine.client import RemoteEngineClient
import threading
import atexit

def main():
    engine = asyncio.get_event_loop().run_until_complete(initialize_speech_engine_connector())
    if settings.settings['network'] != 'server':
        from recognition.commands import monitor
        monitor.start_watching_user_state()
    threading.Thread(target=get_cli_loop(), daemon=True).start()
    engine_server = engine.server if isinstance(engine, EngineProcessHandler) else None
    server.loop.run_forever()

@atexit.register
def shutdown():
    pubsub.publish(topics.STOP_MAIN_PROCESS)

async def initialize_speech_engine_connector():
    network = settings.settings['network']
    if network == 'remote':
        return RemoteEngineClient()
    else:
        is_server = network == 'server'
        return await EngineProcessHandler.create(remote=is_server)

def get_cli_loop():
    no_cli = settings.settings['network'] == 'server'
    if no_cli:
        input_blocker = lambda: input('')
    else:
        main_menu = menu.MainMenu()
        input_blocker = main_menu.start

    def loop_func():
        input_blocker()
        server.loop.call_soon_threadsafe(sys.exit)

    return loop_func


if __name__ == "__main__":
    main()
