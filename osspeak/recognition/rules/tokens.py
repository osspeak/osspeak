import ast

from recognition.actions import pyexpr, asttransform, action
from recognition import api

def action_substitute_validator(expr):
    return not (isinstance(expr.body, ast.BinOp) and isinstance(expr.body.op, ast.BitOr))

class BaseToken:
    pass

class WordToken(BaseToken):
    
    def __init__(self, text):
        self.text = text

class OrToken(BaseToken):
    pass

class GroupingOpeningToken(BaseToken):
    pass

class GroupingClosingToken(BaseToken):
    pass    

class OptionalGroupingOpeningToken(BaseToken):
    pass

class OptionalGroupingClosingToken(BaseToken):
    pass    

class NamedRuleToken(BaseToken):
    
    def __init__(self, name):
        self.name = name

class RepetitionToken(BaseToken):

    def __init__(self, low=0, high=None):
        self.low = low
        self.high = high

class ActionSubstituteToken(BaseToken):
    
    def __init__(self, text, defined_functions=None):
        exprs, self.remaining_text = pyexpr.compile_python_expressions(text, action_substitute_validator, raise_on_error=False)
        if not exprs:
            raise RuntimeError(f'Unable to parse any Python expressions from string:\n{text}')
        self.action = action.Action(exprs, defined_functions)
        self.consumed_char_count = len(text) - len(self.remaining_text)