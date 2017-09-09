import threading
import log
import queue
import platforms.api
from sprecgrammars.functions import library

recognition_queue = queue.Queue()
results_map = {}
builtins = __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)
namespace = {**library.builtin_functions, **builtins}

def get_recognition_result():
    t = threading.current_thread()
    return results_map[t]['recognition']

def recognition_action_worker():
    while True:
        command, recognition_result = recognition_queue.get()
        t = threading.current_thread()
        results_map[t] = {'recognition': recognition_result}
        try:
            for result in command.action.generate_results():
                perform_io(result)
        except KeyError as e:
            log.logger.error(f'Action {command.action.text} errored: {str(e)}')
        finally:
            del results_map[t]

def perform_io(item):
    print('perform io', item)
    if isinstance(item, (str, float, int)):
        return platforms.api.type_literal(item)
    # if not any(isinstance(x, (tuple, list)) for x in items):
    #     return platforms.api.type_keypresses(items)
    # for item in items:
    #     if isinstance(item, (tuple, list)):
    #         perform_io(item)
    #     elif isinstance(item, (int, str, float)):
    #         platforms.api.type_literal(item)
            
workers = [threading.Thread(target=recognition_action_worker, daemon=True) for _ in range(3)]
for worker in workers:
    worker.start()

class RecognitionResult:

    def __init__(self, variables):
        self.vars = VariableList(variables)

class VariableList:

    def __init__(self, variables):
        self._vars = variables

    def get(self, idx, default=None):
        try:
            variable_actions = self._vars[idx]
        except IndexError:
            return default
        return var_result(variable_actions) if variable_actions else default

def var_result(variable_actions):
    results = []
    for action in variable_actions:
        results.append(action.perform())
    return results[0]

def perform_action(command, variable_tree, engine_result):
    log.logger.info(f'Matched rule: {command.rule.raw_text}')
    # empty variables dict, gets filled based on result
    engine_variables = tuple(v for v in engine_result['Variables'] if len(v) == 2)
    var_list = variable_tree.action_variables(engine_variables)
    recognition_result = RecognitionResult(var_list)
    recognition_queue.put((command, recognition_result))

def perform_commands(command_results, command_map):
    log.logger.debug(f'Got commands: {command_results}')
    action_results = []
    for result in command_results:
        command_dict = command_map[result['RuleId']]
        action_result = perform_action(command_dict['command'], command_dict['variable_tree'], result)
    
def save_command_perform_history(action_results):
    if any('threads' in r['result'] for r in action_results):
        threading.Thread(target=join_async_threads, args=[action_results]).start()
    elif all(r['result']['store in history'] for r in action_results):
        history.command_history.append(action_results)

def join_async_threads(action_results):
    for result in action_results:
        for thread in result['result'].get('threads', []):
            thread.join()
    if all(r['result']['store in history'] for r in action_results):
        history.command_history.append(action_results)