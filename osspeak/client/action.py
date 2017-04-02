import log
from sprecgrammars.functions.library import history
from client import action

def perform_action(command, engine_result):
    # empty variables dict, gets filled based on result
    log.logger.info(f'Matched rule: {command.rule.raw_text}')
    engine_variables = tuple(v for v in engine_result['Variables'] if len(v) == 2)
    var_list = command.variable_tree.action_variables(engine_variables)
    try:
        result = command.action.perform(var_list)
        return {'result': result, 'action': command.action, 'variables': var_list}
    except Exception as e:
        log.logger.error(f'Action {command.action.raw_text} errored: {str(e)}')

def perform_commands(command_results, command_map, previous_command_map):
    log.logger.debug(f'Got commands: {command_results}')
    commands = get_matched_commands(command_results, command_map, previous_command_map)
    action_results = []
    for cmd, result in commands:
        action_result = perform_action(cmd, result)
        if action_result is not None:
            action_results.append(action_result)
    save_command_perform_history(action_results)
    
def get_matched_commands(command_results, command_map, previous_command_map):
    commands = []
    for result in command_results:
        try:
            if result['RuleId'] in command_map:
                commands.append([command_map[result['RuleId']], result])
            else:
                commands.append([previous_command_map[result['RuleId']], result])
        except KeyError:
            log.logger.warning(f'Command {result} no longer exists')
    return commands

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