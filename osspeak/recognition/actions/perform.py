import threading
import log
import time
import queue
import contextlib
import platforms.api
from recognition.actions import context

recognition_queue = queue.Queue()
results_map = {}
last_keypress_timestamp = None

def get_recognition_context():
    t = threading.current_thread()
    return results_map[t]['context']

def recognition_action_worker():
    while True:
        command, recognition_context = recognition_queue.get()
        t = threading.current_thread()
        results_map[t] = {'context': recognition_context}
        try:
            evaluation = command.action.perform()
        except Exception as e:
            log.logger.error(f'Action {command.action.text} errored: {str(e)}')
        finally:
            del results_map[t]

workers = [threading.Thread(target=recognition_action_worker, daemon=True) for _ in range(1)]
for worker in workers:
    worker.start()

@contextlib.contextmanager
def keypress_delay():
    global last_keypress_timestamp
    if last_keypress_timestamp is not None:
        diff = time.clock() - last_keypress_timestamp
        time.sleep(max(.05 - diff, 0))
    yield
    last_keypress_timestamp = time.clock()

def perform_io(item):
    if isinstance(item, (str, float, int)):
        with keypress_delay():
            platforms.api.type_literal(item)

def perform_action(command, variable_tree, engine_result):
    log.logger.info(f'Matched rule: {command.rule.raw_text}')
    # empty variables dict, gets filled based on result
    recognition_context = context.create_recognition_context(engine_result, variable_tree)
    recognition_queue.put((command, recognition_context))

def perform_commands(command_results, command_map):
    log.logger.debug(f'Got commands: {command_results}')
    action_results = []
    for result in command_results:
        command_dict = command_map[result['RuleId']]
        action_result = perform_action(command_dict['command'], command_dict['variable_tree'], result)

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