import json
import threading
from communication.procs import EngineProcessManager
from interfaces.gui.guimanager import GuiProcessManager
from interfaces.cli import menu
from client import cmwatcher

class EventDispatcher:

    def __init__(self):
        self.gui_manager = GuiProcessManager(self)
        self.cmd_module_watcher = cmwatcher.CommandModuleWatcher(self)
        self.start_engine_process()
        self.start_module_watcher()

    def start_interface(self, use_gui=True):
        if use_gui:
            self.start_gui()
        else:
            menu.Menu(self).prompt_input()
            event_dispatcher.engine_process.shutdown()

    def start_engine_process(self):
        self.engine_process = EngineProcessManager(self.cmd_module_watcher)
        self.engine_process.start_stdout_listening()

    def start_gui(self):
        self.gui_manager.start_server()

    def start_module_watcher(self):
        self.cmd_module_watcher.initialize_modules()
        self.cmd_module_watcher.start_watch_active_window()

    def main_loop(self):
        menu.Menu(self).prompt_input()