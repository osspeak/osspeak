from sprecgrammars.actions import parser, actionstream

class BaseToken:
    pass

class WordToken(BaseToken):
    
    def __init__(self, text):
        self.text = text

class OrToken(BaseToken):
    pass

class ParenToken(BaseToken):

    def __init__(self, char):
        assert char in '()'
        self.is_open = char == '('

class BracketToken(BaseToken):

    def __init__(self, char):
        assert char in '[]'
        self.is_open = char == '['

class VariableToken(BaseToken):
    
    def __init__(self, name):
        self.name = name

class RepetitionToken(BaseToken):

    def __init__(low=0, high=None):
        self.low = low
        self.high = high

class ActionSubstituteToken(BaseToken):
    
    def __init__(self, text):
        self.text = text
        action_parser = parser.ActionParser(text)
        self.action = action_parser.parse_substitute_action()
        self.consumed_char_count = action_parser.stream.stream.pos