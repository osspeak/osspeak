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


class GreaterThanToken(BaseToken):
    pass

class LessThanToken(BaseToken):
    pass

class RepetitionToken(BaseToken):

    def __init__(low=0, high=None):
        self.low = low
        self.high = high