import threading
import log
from sprecgrammars.functions.library.state import state_copy
from platforms import api
from communication import messages
import time

def create_message_subscriptions(shutdown_event, msg_list):
    messages.subscribe(messages.STOP_MAIN_PROCESS, lambda: shutdown_event.set())
    messages.subscribe(messages.RELOAD_COMMAND_MODULE_FILES, lambda: set_message(msg_list, messages.RELOAD_COMMAND_MODULE_FILES))
    messages.subscribe(messages.RELOAD_GRAMMAR, lambda: set_message(msg_list, messages.RELOAD_GRAMMAR))

def start_watching_user_state(command_module_watcher):
    command_module_watcher.load_initial_user_state()
    shutdown_event = threading.Event()
    msg_list = [None]
    create_message_subscriptions(shutdown_event, msg_list)
    loop_args = (command_module_watcher, shutdown_event, msg_list)
    threading.Thread(target=watch_user_system_state, args=loop_args, daemon=True).start()

def watch_user_system_state(command_module_watcher, shutdown_event, msg_list):
    previous_window = None
    previous_state = state_copy()
    while not shutdown_event.isSet():
        current_window = api.get_active_window_name().lower()
        different_window = current_window != previous_window
        current_state = state_copy()
        different_user_state = previous_state != current_state
        msg = msg_list[0]
        if different_window or different_user_state or msg:
            new_active_modules = command_module_watcher.get_active_modules(current_window, current_state)
            if new_active_modules != command_module_watcher.active_modules:
                reload_files = msg == messages.RELOAD_COMMAND_MODULE_FILES
                command_module_watcher.load_modules(current_window, current_state, reload_files=reload_files)
            elif msg == messages.RELOAD_GRAMMAR:
                command_module_watcher.load_and_send_grammar()
            previous_window = current_window
            previous_state = current_state
            msg_list[0] = None
        shutdown_event.wait(timeout=1)

def set_message(msg_list, msg):
    msg_list[0] = msg