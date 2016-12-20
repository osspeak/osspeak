from sprecgrammars.rules.parser import RuleParser
from sprecgrammars.actions.parser import ActionParser
from sprecgrammars.functions.parser import FunctionDefinitionParser
from sprecgrammars.rules.astree import NamedRuleNode

def rule(text, variables=None):
    parser = RuleParser(text, variables=variables)
    rule_obj = parser.parse_as_rule()
    rule_obj.raw_text = text
    return rule_obj

def action(text, defined_functions=None):
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

def variable(varname, rule_text, varmap):
    return NamedRuleNode(varname, rule_text, varmap)
    