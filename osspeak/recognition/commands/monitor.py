import pywindow
import collections
import log
import asyncio
from recognition.actions.library.state import state_copy
from recognition.commands import loader
from recognition.actions import perform
from communication import topics, pubsub
from profile import Profiler
import time

command_module_state = loader.CommandModuleState()

def create_message_subscriptions(msg_list):
    pubsub.subscribe(topics.RELOAD_COMMAND_MODULE_FILES, lambda: set_message(msg_list, topics.RELOAD_COMMAND_MODULE_FILES))
    pubsub.subscribe(topics.RELOAD_GRAMMAR, lambda: set_message(msg_list, topics.RELOAD_GRAMMAR))
    pubsub.subscribe(topics.PERFORM_COMMANDS,
        lambda grammar_id, words: perform_commands(command_module_state, grammar_id, words))

def start_watching_user_state():
    msg_list = [None]
    command_module_state.populate()
    loader.load_initial_user_state(command_module_state.command_modules)
    engine_status_history = collections.deque([], 10)
    create_message_subscriptions(msg_list)
    fut = watch_user_system_state(msg_list)
    asyncio.ensure_future(fut)

async def watch_user_system_state(msg_list):
    loop = asyncio.get_event_loop()
    previous_window, previous_state = None, state_copy()
    initial_load_done = False
    while True:
        current_window = pywindow.foreground_window().title.lower()
        is_different_window = current_window != previous_window
        current_state = state_copy()
        is_different_user_state = previous_state != current_state
        msg = msg_list[0]
        if is_different_window or is_different_user_state or msg:
            new_active_modules = loader.get_active_modules(command_module_state.command_modules, current_window, current_state)
            reload_files = msg == topics.RELOAD_COMMAND_MODULE_FILES
            if new_active_modules != command_module_state.active_command_modules or reload_files:
                initialize = not initial_load_done or reload_files
                await loader.load_modules(command_module_state, current_window, current_state, initialize=initialize)
                initial_load_done = True
            elif msg == topics.RELOAD_GRAMMAR:
                loader.load_and_send_grammar(command_module_state)
            previous_window = current_window
            msg_list[0] = None
        previous_state = current_state
        await asyncio.sleep(1)

def set_message(msg_list, msg):
    msg_list[0] = msg

def perform_commands(command_module_state: loader.CommandModuleState, grammar_id: str, words):
    try:
        grammar_context = command_module_state.grammars[grammar_id]
    except KeyError:
        log.logger.warning(f'Grammar {grammar_id} no longer exists')
        return
    perform.perform_commands(grammar_context, words)