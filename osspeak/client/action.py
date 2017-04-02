def perform_action(self, command, engine_result):
    # empty variables dict, gets filled based on result
    logger.info(f'Matched rule: {self.rule.raw_text}')
    engine_variables = tuple(v for v in engine_result['Variables'] if len(v) == 2)
    var_list = self.variable_tree.action_variables(engine_variables)
    try:
        result = self.action.perform(var_list)
        return {'result': result, 'action': self.action, 'variables': var_list}
    except Exception as e:
        logger.error(f'Action {self.action.raw_text} errored: {str(e)}')

def perform_commands(self, command_results, command_maps):
    from sprecgrammars.functions.library import history
    log.logger.debug(f'Got commands: {command_results}')
    commands = []
    for result in command_results:
        try:
            if result['RuleId'] in self.command_map:
                commands.append([self.command_map[result['RuleId']], result])
            else:
                commands.append([self.previous_command_map[result['RuleId']], result])
        except KeyError:
            log.logger.warning(f'Command {result} no longer exists')
    action_results = []
    for cmd, result in commands:
        action_result = perform_action(cmd, result)
        if action_result is not None:
            action_results.append(action_result)
    if all(r['result']['store in history'] for r in action_results):
        history.command_history.append(action_results)
    