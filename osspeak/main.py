import argparse

from client import dispatcher
from communication import server, client, messages
from interfaces.cli import menu
from settings import usersettings
from interfaces.gui.guimanager import GuiProcessManager
from client import cmwatcher
from communication.procs import EngineProcessManager

def main():
    user_settings = usersettings.load_user_config()
    print(user_settings)
    return
    clargs = get_args()
    if clargs.engine_server:
        server.RemoteEngineServer().loop_forever()
        return
    bootup(clargs)

def bootup(clargs):
    ui_manager = GuiProcessManager() if clargs.interface == 'gui' else menu.Menu()
    cmw = cmwatcher.CommandModuleWatcher()
    if clargs.engine_location == 'local':
        EngineProcessManager()
    else:
        client.RemoteEngineClient().loop_forever()
    cmw.initialize_modules()
    cmw.start_watch_active_window()
    ui_manager.main_loop()
    messages.dispatch('shutdown')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', default='remote')
    parser.add_argument('--engine_location', default='local') # or remote
    parser.add_argument('--engine_server', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    main()