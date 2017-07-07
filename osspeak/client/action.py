import log
import threading
from sprecgrammars.functions.library import history
from client import action

def perform_action(command, variable_tree, engine_result):
    log.logger.info(f'Matched rule: {command.rule.raw_text}')
    # empty variables dict, gets filled based on result
    engine_variables = tuple(v for v in engine_result['Variables'] if len(v) == 2)
    var_list = variable_tree.action_variables(engine_variables)
    try:
        result = command.action.perform(var_list)
        return {'result': result, 'action': command.action, 'variables': var_list}
    except Exception as e:
        log.logger.error(f'Action {command.action.raw_text} errored: {str(e)}')

def perform_commands(command_results, command_map):
    log.logger.debug(f'Got commands: {command_results}')
    action_results = []
    for result in command_results:
        command_dict = command_map[result['RuleId']]
        action_result = perform_action(command_dict['command'], command_dict['variable_tree'], result)
        if action_result is not None:
            action_results.append(action_result)
    save_command_perform_history(action_results)
    
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