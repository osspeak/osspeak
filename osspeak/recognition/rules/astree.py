import collections
import copy

class ASTNode:

    def walk(self):
        yield self

class Rule(ASTNode):

    def __init__(self, name=None):
        self.name = name
        self.children = []
        self.open = True
        self.root = GroupingNode()

    def walk(self, ancestors=None, rules=None):
        yield self
        yield from self.root.walk()

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
        self.sequences = []

    def walk(self):
        yield self
        for seq in self.sequences:
            for node in seq:
                yield from node.walk()

class RuleReference(ASTNode):

    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_substitute = None