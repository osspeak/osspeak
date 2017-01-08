import collections
import uuid


class ASTNode:
    def __init__(self):
        # xml attributes must start with letter so prefix id with 'r'
        self._id = str(uuid.uuid4()).replace('-', '')

    @property
    def id(self):
        return f'r{self._id}'

class GrammarNode(ASTNode):
     
     def __init__(self):
         super().__init__()
         self.rules = []
         self.variables = []

class Rule(ASTNode):

    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.children = []
        self.repeat_low = 1
        self.repeat_high = 1
        self.open = True
        self.is_variable = False
        self.groupings = collections.OrderedDict()

class WordNode(ASTNode):

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_substitute = None

    @property
    def is_single(self):
        return self.repeat_low == 1 and self.repeat_high == 1

    @property
    def id(self):
        prefix = 'w-' if self.action_substitute is None else 's'
        return f'{prefix}{self._id}'

class OrNode(ASTNode):
    pass

class GroupingNode(ASTNode):

    def __init__(self):
        super().__init__()
        self.children = []
        self.open = True
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_substitute = None