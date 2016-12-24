import collections
import uuid


class ASTNode:
    def __init__(self):
        # xml attributes must start with letter so prefix id with 'r'
        self._id = str(uuid.uuid4()).replace('-', '')

    @property
    def id(self):
        return 'r{}'.format(self._id)

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
        self.grouping_variables = collections.OrderedDict()
        # make a copy in perform_action to keep track of string values
        self.grouping_variables_empty = collections.OrderedDict()
        self.open = True
        self.is_variable = False

    # @property
    # def id(self):
    #     return '{}{}'.format('v' if self.is_variable else 'r', self._id)

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
        return '{}{}'.format('' if self.action_substitute is None else 's', self._id)

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
        self.child_ids = {}