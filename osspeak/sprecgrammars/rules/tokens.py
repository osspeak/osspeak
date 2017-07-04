from sprecgrammars.actions import parser, actionstream

class BaseToken:
    pass

class WordToken(BaseToken):
    
    def __init__(self, text):
        self.text = text

class OrToken(BaseToken):
    pass

class GroupingOpeningToken(BaseToken):
    CHARACTER = '('

class GroupingClosingToken(BaseToken):
    CHARACTER = ')'    

class OptionalGroupingOpeningToken(BaseToken):
    CHARACTER = '['

class OptionalGroupingClosingToken(BaseToken):
    CHARACTER = ']'    

class NamedRuleToken(BaseToken):
    
    def __init__(self, name):
        self.name = name

class RepetitionToken(BaseToken):

    def __init__(self, low=0, high=None):
        self.low = low
        self.high = high

class ActionSubstituteToken(BaseToken):
    
    def __init__(self, text, defined_functions=None):
        self.text = text
        action_parser = parser.ActionParser(text, defined_functions=defined_functions)
        self.action = action_parser.parse(substitute=True)
        self.consumed_char_count = sum(t.character_count for t in action_parser.parsed_tokens)