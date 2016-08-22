class ActionToken:
    pass

class LiteralToken(ActionToken):
    
    def __init__(self, text):
        self.text = text