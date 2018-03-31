def rule(text, name=None):
    from recognition.rules.parser import RuleParser
    parser = RuleParser(text)
    rule_obj = parser.parse_as_rule(name=name)
    rule_obj.raw_text = text
    return rule_obj

def action(text):
    from recognition.actions.action import Action
    return Action(text)

def function(func_signature, func_action=None):
    from recognition.actions.function import Function
    func = Function(func_signature, func_action)
    return func