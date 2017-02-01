import argparse

import log
from client import dispatcher
from communication import server, client, messages
from interfaces.cli import menu
from user import settings
from interfaces.gui.guimanager import GuiProcessManager
from client import cmwatcher
from communication.procs import EngineProcessManager

def main():
    print(settings.user_settings)
    clargs = get_args()
    if settings.user_settings['engine_server']:
        server.RemoteEngineServer().loop_forever()
        return
    bootup(clargs)

def bootup(clargs):
    ui_manager = GuiProcessManager() if clargs.interface == 'gui' else menu.Menu()
    if settings.user_settings['network'] == 'local':
        ref = EngineProcessManager()
    else:
        ref = client.RemoteEngineClient().connect()
    cmw = cmwatcher.CommandModuleWatcher()
    cmw.initialize_modules()
    cmw.start_watch_active_window()
    ui_manager.main_loop()
    ref.socket.close()
    messages.dispatch('shutdown')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', default='remote')
    parser.add_argument('--network', default='local') # or remote
    parser.add_argument('--engine_server', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    main()