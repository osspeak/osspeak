def rule(text, name=None):
    from recognition.rules.parser import RuleParser
    parser = RuleParser(text)
    rule_obj = parser.parse_as_rule(name=name)
    rule_obj.raw_text = text
    return rule_obj

def action(action_input, *args, **kwargs):
    from recognition.actions.action import Action, SpeechDSLAction, PythonFunctionAction
    if isinstance(action_input, str):
        return SpeechDSLAction(action_input, *args, **kwargs)
    elif isinstance(action_input, dict) and action_input['type'] == 'python':
        return PythonFunctionAction(action_input['data'], *args, **kwargs)
    raise TypeError

def function(func_signature, func_action=None):
    from recognition.actions.function import Function
    func = Function(func_signature, func_action)
    return func