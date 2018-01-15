from recognition.rules.parser import RuleParser
from recognition.actions import action, pyexpr, asttransform
from recognition.actions.action import Action
from recognition.actions.function import Function

def rule(text, name=None):
    parser = RuleParser(text)
    rule_obj = parser.parse_as_rule(name=name)
    rule_obj.raw_text = text
    return rule_obj

def action(text):
    return Action(text)

def function(func_signature, func_action=None, defined_functions=None):
    func = Function(func_signature, func_action)
    return func