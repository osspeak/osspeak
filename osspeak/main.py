import argparse

import log
import clargs
from client import dispatcher
from communication import server, client, messages
from interfaces.cli import menu
from user import settings
from interfaces.gui.guimanager import GuiProcessManager
from client import cmwatcher
from communication.procs import EngineProcessManager

def main():
    args = clargs.args
    if settings.user_settings['network'] == 'server':
        server.RemoteEngineServer().loop_forever()
        return
    use_gui = settings.user_settings['interface'] == 'gui'
    ui_manager = GuiProcessManager() if use_gui else menu.MainMenu()
    io_obj = get_io()
    try:
        cmw = cmwatcher.CommandModuleWatcher()
        cmw.initialize_modules()
        cmw.start_watch_active_window()
        ui_manager.main_loop()
    finally:
        messages.dispatch_sync(messages.ENGINE_STOP)
        io_obj.socket.close()


def get_io():
    if settings.user_settings['network'] == 'local':
        return EngineProcessManager()
    else:
        engine_client = client.RemoteEngineClient()
        engine_client.connect()
        return engine_client

if __name__ == "__main__":
    main()