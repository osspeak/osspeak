import threading
import log
import asyncio
from recognition.actions.library.state import state_copy
from recognition.commands import loader
from recognition.actions import perform
from platforms import api
from communication import topics, pubsub
from profile import Profiler
import time

def create_message_subscriptions(shutdown_event, msg_list, cache):
    pubsub.subscribe(topics.RELOAD_COMMAND_MODULE_FILES, lambda: set_message(msg_list, topics.RELOAD_COMMAND_MODULE_FILES))
    pubsub.subscribe(topics.RELOAD_GRAMMAR, lambda: set_message(msg_list, topics.RELOAD_GRAMMAR))
    pubsub.subscribe(topics.PERFORM_COMMANDS, lambda command_results, grammar_id: perform_commands(cache, command_results, grammar_id))

def start_watching_user_state():
    shutdown_event = threading.Event()
    msg_list = [None]
    cache = loader.CommandModuleCache()
    cache.populate()
    loader.load_initial_user_state(cache.command_modules)
    create_message_subscriptions(shutdown_event, msg_list, cache)
    fut = watch_user_system_state(msg_list, cache)
    asyncio.ensure_future(fut)

async def watch_user_system_state(msg_list, cache):
    loop = asyncio.get_event_loop()
    previous_window, previous_state = None, state_copy()
    while True:
        current_window = api.get_active_window_name().lower()
        is_different_window = current_window != previous_window
        current_state = state_copy()
        is_different_user_state = previous_state != current_state
        msg = msg_list[0]
        if is_different_window or is_different_user_state or msg:
            new_active_modules = loader.get_active_modules(cache.command_modules, current_window, current_state)
            if new_active_modules != cache.active_command_modules:
                reload_files = msg == topics.RELOAD_COMMAND_MODULE_FILES
                await loader.load_modules(cache, current_window, current_state)
            elif msg == topics.RELOAD_GRAMMAR:
                loader.load_and_send_grammar(cache)
            previous_window = current_window
            previous_state = current_state
            msg_list[0] = None
        await asyncio.sleep(1)

def set_message(msg_list, msg):
    msg_list[0] = msg

def perform_commands(cache, command_results, grammar_id):
    try:
        command_map = cache.grammar_commands[grammar_id]
    except KeyError:
        log.logger.warning(f'Grammar {grammar_id} no longer exists')
        return
    perform.perform_commands(command_results, command_map)