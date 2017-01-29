import argparse

from client import dispatcher
from communication import server, client, messages
from interfaces.cli import menu
from interfaces.gui.guimanager import GuiProcessManager
from client import cmwatcher
from communication.procs import EngineProcessManager

def main():
    clargs = get_args()
    if clargs.engine_server:
        server.RemoteEngineServer().loop_forever()
        # client.RemoteEngineClient().loop_forever()
        return
    if clargs.interface == 'remote':
        return
    bootup(clargs)

def bootup(clargs):
    ui_manager = GuiProcessManager() if clargs == 'gui' else menu.Menu()
    cmw = cmwatcher.CommandModuleWatcher()
    EngineProcessManager().start_stdout_listening()
    cmw.initialize_modules()
    cmw.start_watch_active_window()
    ui_manager.main_loop()
    messages.dispatch('shutdown')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', default='cli')
    parser.add_argument('--engine_server', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    main()