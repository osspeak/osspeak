class FunctionDefinitionBase:
    pass

class FunctionDefinition(FunctionDefinitionBase):

    def __init__(self):
        self.name = None
        self.parameters = []
        self.args_name = None
        self.kwargs_name = None
        self.action = None

class FunctionParameter(FunctionDefinitionBase):
    
    def __init__(self, name):
        self.name = name
        self.default_action = None