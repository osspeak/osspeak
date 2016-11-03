from sprecgrammars.formats.rules.parser import RuleParser
from sprecgrammars.actions.parser import ActionParser
from sprecgrammars.functions.parser import FunctionDefinitionParser

def rule(text, variables=None):
    parser = RuleParser(text, variables=variables)
    return parser.parse_as_rule()

def action(text, defined_functions=None):
    parser = ActionParser(text, defined_functions=defined_functions)
    return parser.parse()

def func_definition(func_signature, func_action=''):
    parser = FunctionDefinitionParser(func_signature)
    func_def = parser.parse()
    action_parser = ActionParser(func_action)
    func_def.action = action_parser.parse()
    return func_def