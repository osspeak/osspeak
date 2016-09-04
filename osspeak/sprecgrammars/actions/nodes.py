from platforms import api

class Action:

    def add(self, *a, **k):
        raise NotImplementedError

class RootAction(Action):

    def __init__(self):
        self.children = []

    def add(self, child):
        self.children.append(child)

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

class FunctionCall(Action):

    def __init__(self, func_name):
        self.arguments = []
        self.func_name = func_name
        self.expecting_comma = False

    def add(self, node):
        self.arguments.append(node)