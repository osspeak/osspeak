import pywindow
import time
import threading
import collections
import log
import copy
import settings
import clargs
from recognition.commands import loader
from recognition.actions import perform
from communication import topics, pubsub
import time


def create_message_subscriptions(msg_list, command_module_controller):
    pubsub.subscribe(topics.RELOAD_COMMAND_MODULE_FILES, lambda: set_message(msg_list, topics.RELOAD_COMMAND_MODULE_FILES))
    pubsub.subscribe(topics.RELOAD_GRAMMAR, lambda: set_message(msg_list, topics.RELOAD_GRAMMAR))
    pubsub.subscribe(topics.PERFORM_COMMANDS,
        lambda grammar_id, words: perform_commands(command_module_controller, grammar_id, words))

def start_watching_user_state():
    msg_list = [None]
    command_module_file_pattern = clargs.get_args()['file_pattern']
    module_loader = loader.StaticFileCommandModuleLoader(settings.settings['command_directory'], command_module_file_pattern)
    command_module_controller = loader.CommandModuleController(module_loader)
    command_module_controller.command_modules = command_module_controller.initialize_command_modules()
    engine_status_history = collections.deque([], 10)
    create_message_subscriptions(msg_list, command_module_controller)
    threading.Thread(target=watch_user_system_state, daemon=True, args=(msg_list, command_module_controller)).start()

def watch_user_system_state(msg_list, command_module_controller):
    from recognition.actions.library.stdlib import namespace
    previous_window = None
    previous_state = None
    initial_load_done = False
    while True:
        current_state = copy.copy(namespace['state'])
        current_window = pywindow.foreground_window().title.lower()
        is_different_window = current_window != previous_window
        is_different_state = current_state != previous_state
        msg = msg_list[0]
        if is_different_window or is_different_state or msg:
            msg_list[0] = None
            new_active_modules = command_module_controller.get_active_modules(current_window)
            reload_files = msg == topics.RELOAD_COMMAND_MODULE_FILES
            if new_active_modules != command_module_controller.active_command_modules or reload_files:
                initialize_modules = not initial_load_done or reload_files
                command_module_controller.load_modules(current_window, initialize_modules=False)
                initial_load_done = True
            elif msg == topics.RELOAD_GRAMMAR:
                raise NotImplementedError
                command_module_controller.load_and_send_grammar()
            previous_window = current_window
            previous_state = current_state
        time.sleep(1)

def set_message(msg_list, msg):
    msg_list[0] = msg

def perform_commands(command_module_controller: loader.CommandModuleController, grammar_id: str, words):
    try:
        grammar_context = command_module_controller.grammars[grammar_id]
    except KeyError:
        log.logger.warning(f'Grammar {grammar_id} no longer exists')
        return
    perform.perform_commands(grammar_context, words)