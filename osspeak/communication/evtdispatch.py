import json
import threading
from communication.procs import EngineProcessManager
from interfaces.gui.guimanager import GuiProcessManager
from interfaces.cli import menu
from client import cmwatcher

class EventDispatcher:

    def __init__(self, clargs):
        self.shutdown = threading.Event()
        self.clargs = clargs
        if self.clargs.interface == 'gui':
            self.ui_manager = GuiProcessManager(self)
        self.cmd_module_watcher = cmwatcher.CommandModuleWatcher(self)
        self.start_engine_process()
        self.start_module_watcher()

    def start_interface(self):
        if self.clargs.interface == 'gui':
            self.start_gui()
        elif self.clargs.interface == 'cli':
            self.ui_manager = menu.Menu(self)
            self.ui_manager.main_loop()
            self.shutdown.set()
            # self.engine_process.shutdown()

    def start_engine_process(self):
        self.engine_process = EngineProcessManager(self)
        self.engine_process.start_stdout_listening()

    def start_gui(self):
        self.ui_manager.start_server()

    def start_module_watcher(self):
        self.cmd_module_watcher.initialize_modules()
        self.cmd_module_watcher.start_watch_active_window()

    def main_loop(self):
        menu.Menu(self).prompt_input()

    def route_message(self, recepient, msgkey, payload):
        if recepient == 'ui':
            self.ui_manager.send_message(msgkey, payload)