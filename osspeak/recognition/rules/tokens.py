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
        self.action = action.Action(text, defined_functions, validator=action_substitute_validator, raise_on_error=False)
        if not self.action.expressions:
            raise RuntimeError(f'Unable to parse any Python expressions from string:\n{text}')
        self.consumed_char_count = len(text) - len(self.action.remaining_text)
        print(self.consumed_char_count, text, self.action.remaining_text)