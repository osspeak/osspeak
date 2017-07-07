import collections
import uuid
import copy

class ASTNode:

    def walk(self):
        yield self
        for child in getattr(self, 'children', []):
            yield from child.walk()
            
class Rule(ASTNode):

    def __init__(self, name=None):
        self.name = name
        self.children = []
        self.base_rule = None
        self.repeat_low = 1
        self.repeat_high = 1
        self.open = True

    def create_reference(self):
        reference_rule = copy.copy(self)
        reference_rule.base_rule = self
        reference_rule._id = str(uuid.uuid4()).replace('-', '')
        return reference_rule

class WordNode(ASTNode):

    def __init__(self, text):
        self.text = text
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_substitute = None

    @property
    def is_single(self):
        return self.repeat_low == 1 and self.repeat_high == 1

class OrNode(ASTNode):
    pass

class GroupingNode(ASTNode):

    def __init__(self):
        self.children = []
        self.open = True
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_substitute = None