import threading
import log
from sprecgrammars.functions.library.state import state_copy
from platforms import api
from communication import messages
import time

reload_files = False
reload_grammar = False

def create_message_subscriptions(shutdown_event):
    messages.subscribe(messages.STOP_MAIN_PROCESS, lambda: shutdown_event.set())
    messages.subscribe(messages.RELOAD_COMMAND_MODULE_FILES, set_reload_files_flag)
    messages.subscribe(messages.RELOAD_GRAMMAR, set_reload_grammar_flag)

def start_watching_user_state(command_module_watcher):
    command_module_watcher.load_initial_user_state()
    shutdown_event = threading.Event()
    create_message_subscriptions(shutdown_event)
    loop_args = (command_module_watcher, shutdown_event)
    threading.Thread(target=watch_user_system_state, args=loop_args, daemon=True).start()

def watch_user_system_state(command_module_watcher, shutdown_event):
    global reload_files
    previous_window = None
    previous_state = state_copy()
    while not shutdown_event.isSet():
        current_window = api.get_active_window_name().lower()
        different_window = current_window != previous_window
        current_state = state_copy()
        different_user_state = previous_state != current_state
        if different_window or different_user_state or reload_files or reload_grammar:
            new_active_modules = command_module_watcher.get_active_modules(current_window, current_state)
            if new_active_modules != command_module_watcher.active_modules:
                command_module_watcher.load_modules(current_window, current_state, reload_files=reload_files)
            elif reload_grammar:
                command_module_watcher.load_and_send_grammar()
            previous_window = current_window
            previous_state = current_state
            reload_files = False
            reload_grammar = False
        shutdown_event.wait(timeout=1)

def set_reload_files_flag():
    global reload_files
    reload_files = True

def set_reload_grammar_flag():
    global reload_grammar
    reload_grammar = True