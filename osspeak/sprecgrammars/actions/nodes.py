from platforms import api

class Action:

    def __init__(self):
        self.children = []

    def perform(self):
        print(self.children)
        for subaction in self.children:
            subaction.perform()

class LiteralKeysAction(Action):
    
    def __init__(self, text):
        super().__init__()
        self.text = text

    def perform(self):
        print(self.text)
        api.type_literal(self.text)

def FunctionCall(Action):

    def __init__(self):
        self.arguments = []