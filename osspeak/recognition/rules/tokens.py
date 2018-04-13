import ast

from recognition.actions import pyexpr, asttransform, action, piece

def action_substitute_validator(expr):
    return not (isinstance(expr.body, ast.BinOp) and isinstance(expr.body.op, ast.BitOr))

class BaseToken:
    
    def __init__(self, *args, **kwargs):
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

class WhitespaceToken(BaseToken):

    def __init__(self, text): 
        self.text = text

class NamedRuleToken(BaseToken):
    
    def __init__(self, name):
        self.name = name

class RepetitionToken(BaseToken):

    def __init__(self, low=0, high=None):
        self.low = low
        self.high = high

class ActionSubstituteToken(BaseToken):
    
    def __init__(self, text):
        self.action_piece = piece.DSLActionPiece(text, validator=action_substitute_validator, raise_on_error=False)
        if not self.action_piece.expressions:
            raise RuntimeError(f'Unable to parse any Python expressions from string:\n{text}')
        self.consumed_char_count = len(text) - len(self.action_piece.remaining_text)