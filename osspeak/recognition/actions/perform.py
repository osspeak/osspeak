import threading
import log
import time
import queue
import keyboard
from settings import settings
import platforms.api
from recognition.actions import context

recognition_queue = queue.Queue()
results_map = {}

def get_recognition_context():
    t = threading.current_thread()
    return results_map[t]['context']

def recognition_action_worker():
    while True:
        action, recognition_context = recognition_queue.get()
        t = threading.current_thread()
        results_map[t] = {'context': recognition_context}
        try:
            evaluation = action.perform()
        except Exception as e:
            log.logger.error(f'Action {action.text} errored: {str(e)}')
        finally:
            del results_map[t]

worker = threading.Thread(target=recognition_action_worker, daemon=True)
worker.start()

def perform_io(item):
    if isinstance(item, (str, float, int)):
        keyboard.write(str(item))
        return True
    return False

def perform_action_from_event(action, namespace):
    recognition_context = context.create_event_context(namespace)
    recognition_queue.put((action, recognition_context))

def perform_action(command, variable_tree, namespace, engine_result):
    log.logger.info(f'Matched rule: {command.rule.raw_text}')
    # empty variables dict, gets filled based on result
    recognition_context = context.create_recognition_context(engine_result, variable_tree, namespace)
    recognition_queue.put((command.action, recognition_context))

def perform_commands(command_results, command_map):
    log.logger.debug(f'Got commands: {command_results}')
    action_results = []
    for result in command_results:
        command_dict = command_map[result['RuleId']]
        action_result = perform_action(command_dict['command'], command_dict['variable_tree'],
            command_dict['namespace'], result)

def var_result(variable_actions, perform_results):
    results = []
    for action in variable_actions:
        results.append(action.perform_variable(perform_results=perform_results))
    if not perform_results:
        return concat_results(results)

def concat_results(results):
    acc = None
    for res in results:
        if acc is None:
            acc = res
        else:
            try:
                acc += res
            except TypeError:
                pass
    return acc