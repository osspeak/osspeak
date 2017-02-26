class ActionToken:
    
    @property
    def character_count(self):
        return 1

class WordToken(ActionToken):
    
    def __init__(self, text):
        self.text = text

    @property
    def character_count(self):
        return len(self.text)

class LiteralToken(ActionToken):
    
    def __init__(self, text):
        self.text = text

    @property
    def character_count(self):
        return len(self.text) + 2

class LiteralTemplateToken(ActionToken):

    DELIMITER = '`'
    
    def __init__(self, text):
        self.text = text

    @property
    def character_count(self):
        return len(self.text) + 2

class GroupingOpeningToken(ActionToken):
    CHARACTER = '('

class GroupingClosingToken(ActionToken):
    CHARACTER = ')'

class BraceToken(ActionToken):
    
    def __init__(self, ch):
        self.is_open = ch == '{'

class CommaToken(ActionToken):

    def __init__(self):
        self.text = ','

class PlusToken(ActionToken):
    
    def __init__(self):
        self.text = '+'

class PositionalVariableToken(ActionToken):

    def __init__(self, pos):
        self.pos = pos

class NamedVariableToken(ActionToken):

    def __init__(self, name):
        self.name = name

class UnderscoreToken(ActionToken):

    def __init__(self):
        pass

class WhitespaceToken(ActionToken):

    def __init__(self, text):
        self.text = text

    @property
    def character_count(self):
        return len(self.text)

class SliceToken(ActionToken):

    OPENING_DELIMITER = '['
    CLOSING_DELIMITER = ']'

    def __init__(self, pieces):
        self.pieces = pieces

    @property
    def character_count(self):
        return sum((p for p in self.pieces), key=len) + len(self.pieces) + 1