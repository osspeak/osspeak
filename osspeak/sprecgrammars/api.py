from sprecgrammars.rules.parser import RuleParser
from sprecgrammars.actions.parser import ActionParser
from sprecgrammars.actions.action import Action
from sprecgrammars.functions.parser import FunctionDefinitionParser
from sprecgrammars.functions.parser import FunctionDefinitionParser
from sprecgrammars.function import Function
from sprecgrammars.actions import pyexpr, asttransform

def rule(text, name=None, rules=None, defined_functions=None):
    parser = RuleParser(text, rules=rules, defined_functions=defined_functions)
    print('text: ', text)
    rule_obj = parser.parse_as_rule(name=name)
    rule_obj.raw_text = text
    return rule_obj

def action(text, defined_functions=None):
    return Action(text, defined_functions)
    parser = ActionParser(text, defined_functions=defined_functions)
    action_obj = parser.parse()
    action_obj.raw_text = text
    return action_obj

def func_definition(func_signature, func_action=None, defined_functions=None):
    parser = FunctionDefinitionParser(func_signature)
    func_def = parser.parse()
    func_def.raw_text = func_signature
    if func_action is not None:
        func_def.action = action(func_action, defined_functions=defined_functions)
    return func_def

def function(func_signature, func_action=None, defined_functions=None):
    func = Function(func_signature, func_action)
    return func