import uuid

class ASTNode:
    def __init__(self):
        # xml attributes must start with letter so prefix id with 'r'
        self.id = 'r' + str(uuid.uuid4()).replace('-', '')

class GrammarNode(ASTNode):
     
     def __init__(self):
         super().__init__()
         self.rules = []

class Rule(ASTNode):

    def __init__(self):
        super().__init__()
        self.children = []
        self.open = True

class WordNode(ASTNode):

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.repeat_low = 1
        self.repeat_high = 1

    @property
    def is_single(self):
        return self.repeat_low == 1 and self.repeat_high == 1

class OrNode(ASTNode):
    pass

class GroupingNode(ASTNode):

    def __init__(self):
        super().__init__()
        self.children = []
        self.open = True
        self.repeat_low = 1
        self.repeat_high = 1