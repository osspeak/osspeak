import argparse

from client import dispatcher
from communication import evtdispatch, server, client
from interfaces.cli import menu

def main():
    clargs = get_args()
    if clargs.r:
        client.RemoteEngineClient().loop_forever()
        return
    if clargs.interface == 'remote':
        server.RemoteEngineServer().loop_forever()
        return
    event_dispatcher = evtdispatch.EventDispatcher(clargs)
    event_dispatcher.start_interface()

def bootup(clargs):
    if clargs.interface == 'gui':
        self.ui_manager = GuiProcessManager(self)
    self.cmd_module_watcher = cmwatcher.CommandModuleWatcher(self)
    self.start_engine_process()
    self.start_module_watcher()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', default='remote')
    parser.add_argument('-r', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    main()