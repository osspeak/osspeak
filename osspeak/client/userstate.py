import threading
import log
from recognition.actions.library.state import state_copy
from recognition.commands import loader
from recognition.actions import perform
from platforms import api
from communication import messages
from profile import Profiler
import time

def create_message_subscriptions(shutdown_event, msg_list, cache):
    messages.subscribe(messages.STOP_MAIN_PROCESS, lambda: shutdown_event.set())
    messages.subscribe(messages.RELOAD_COMMAND_MODULE_FILES, lambda: set_message(msg_list, messages.RELOAD_COMMAND_MODULE_FILES))
    messages.subscribe(messages.RELOAD_GRAMMAR, lambda: set_message(msg_list, messages.RELOAD_GRAMMAR))
    messages.subscribe(messages.PERFORM_COMMANDS, lambda command_results, grammar_id: perform_commands(cache, command_results, grammar_id))

def start_watching_user_state():
    # command_module_watcher.load_initial_user_state()
    shutdown_event = threading.Event()
    msg_list = [None]
    cache = loader.CommandModuleCache()
    cache.populate()
    loader.load_initial_user_state(cache.command_modules)
    create_message_subscriptions(shutdown_event, msg_list, cache)
    loop_args = (shutdown_event, msg_list, cache)
    threading.Thread(target=watch_user_system_state, args=loop_args, daemon=True).start()

def watch_user_system_state(shutdown_event, msg_list, cache):
    previous_window = None
    previous_state = state_copy()
    while not shutdown_event.isSet():
        current_window = api.get_active_window_name().lower()
        different_window = current_window != previous_window
        current_state = state_copy()
        different_user_state = previous_state != current_state
        msg = msg_list[0]
        if different_window or different_user_state or msg:
            new_active_modules = loader.get_active_modules(cache.command_modules, current_window, current_state)
            if new_active_modules != cache.active_command_modules:
                reload_files = msg == messages.RELOAD_COMMAND_MODULE_FILES
                loader.load_modules(cache, current_window, current_state, reload_files=reload_files)
            elif msg == messages.RELOAD_GRAMMAR:
                loader.load_and_send_grammar(cache)
            previous_window = current_window
            previous_state = current_state
            msg_list[0] = None
        shutdown_event.wait(timeout=1)

def set_message(msg_list, msg):
    msg_list[0] = msg

def perform_commands(cache, command_results, grammar_id):
    try:
        command_map = cache.grammar_commands[grammar_id]
    except KeyError:
        log.logger.warning(f'Grammar {grammar_id} no longer exists')
        return
    perform.perform_commands(command_results, command_map)