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
    pass

class PlusToken(ActionToken):
    pass