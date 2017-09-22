import threading
import log
import time
import queue
import contextlib
import platforms.api
from sprecgrammars.functions import library

recognition_queue = queue.Queue()
results_map = {}
last_keypress_timestamp = None
builtins = __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)
namespace = {**library.builtin_functions, **builtins}


def get_recognition_result():
    t = threading.current_thread()
    return results_map[t]['recognition']

def recognition_action_worker():
    while True:
        command, recognition_context = recognition_queue.get()
        t = threading.current_thread()
        results_map[t] = {'recognition': recognition_context}
        try:
            evaluation = command.action.perform()
        except KeyError as e:
            log.logger.error(f'Action {command.action.text} errored: {str(e)}')
        finally:
            del results_map[t]

workers = [threading.Thread(target=recognition_action_worker, daemon=True) for _ in range(1)]
for worker in workers:
    worker.start()

class RecognitionContext:

    def __init__(self, variables):
        self.vars = VariableList(variables)

class VariableList:

    def __init__(self, variables):
        self._vars = variables

    def get(self, idx, default=None, perform_results=True):
        try:
            variable_actions = self._vars[idx]
        except IndexError as e:
            raise e
            return default
        return var_result(variable_actions, perform_results) if variable_actions else default

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

def perform_action(command, variable_tree, engine_result):
    log.logger.info(f'Matched rule: {command.rule.raw_text}')
    # empty variables dict, gets filled based on result
    engine_variables = tuple(v for v in engine_result['Variables'] if len(v) == 2)
    var_list = variable_tree.action_variables(engine_variables)
    recognition_result = RecognitionContext(var_list)
    recognition_queue.put((command, recognition_result))

def perform_commands(command_results, command_map):
    log.logger.debug(f'Got commands: {command_results}')
    action_results = []
    for result in command_results:
        command_dict = command_map[result['RuleId']]
        action_result = perform_action(command_dict['command'], command_dict['variable_tree'], result)