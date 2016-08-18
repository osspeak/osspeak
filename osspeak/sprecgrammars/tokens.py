class BaseToken:
    pass

class WordToken(BaseToken):
    
    def __init__(self, text):
        self.text = text

class OrToken(BaseToken):
    pass

class ParenToken(BaseToken):

    def __init__(self, is_open):
        self.is_open = is_open