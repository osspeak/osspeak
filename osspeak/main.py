import asyncio
import sys

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

import log
from recognition.commands import monitor
from communication import server, pubsub, topics
import settings
from interfaces.cli import menu
from engine.handler import EngineProcessHandler
from engine.client import RemoteEngineClient
import threading
import atexit

def main():
    engine = asyncio.get_event_loop().run_until_complete(initialize_speech_engine_connector())
    if settings.settings['network'] != 'server':
        monitor.start_watching_user_state()
    threading.Thread(target=get_cli_loop(), daemon=True).start()
    engine_server = engine.server if isinstance(engine, EngineProcessHandler) else None
    ws_handlers = server.get_websocket_handlers(engine_server)
    if ws_handlers:
        server.loop.run_until_complete(server.start_websockets(ws_handlers))
    server.loop.run_forever()

@atexit.register
def shutdown():
    pubsub.publish(topics.STOP_MAIN_PROCESS)
    for task in asyncio.Task.all_tasks():
        task.cancel()
    server.loop.stop()

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
        input_blocker = menu.MainMenu().start

    def loop_func():
        input_blocker()
        server.loop.call_soon_threadsafe(sys.exit)

    return loop_func


if __name__ == "__main__":
    main()
