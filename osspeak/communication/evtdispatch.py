import json
from communication.procs import EngineProcessManager
from client import cmwatcher

class EventDispatcher:

    def __init__(self):
        self.cmd_module_watcher = cmwatcher.CommandModuleWatcher()
        self.start_engine_process()
        self.start_module_watcher()
        self.engine_process.start_engine_listening()

    def start_engine_process(self):
        self.engine_process = EngineProcessManager(self.cmd_module_watcher)
        self.engine_process.start_stdout_listening()

    def start_module_watcher(self):
        self.cmd_module_watcher.create_grammar_output()
        self.cmd_module_watcher.start_watch_active_window(self.engine_process.start_engine_listening)

    def main_loop(self):
        menu.Menu(self).prompt_input()