class ActionToken:
    pass

class WordToken(ActionToken):
    
    def __init__(self, text):
        self.text = text

class LiteralToken(ActionToken):
    
    def __init__(self, text):
        self.text = text

class ParenToken(ActionToken):
    
    def __init__(self, ch):
        self.is_open = ch == '('

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

class UnderscoreToken(ActionToken):

    def __init__(self):
        pass

class WhitespaceToken(ActionToken):

    def __init__(self, text):
        self.text = text