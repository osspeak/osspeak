import collections
import copy

class ASTNode:

    def walk(self, ancestors=None, rules=None):
        ancestors = ancestors or []
        rules = rules or {}
        new_ancestors = ancestors + [self]
        for child in getattr(self, 'children', []):
            yield from child.walk(new_ancestors, rules)
        yield {'node': self, 'ancestors': tuple(ancestors)}
            
class Rule(ASTNode):

    def __init__(self, name=None):
        self.name = name
        self.children = []
        self.open = True
        self.root = GroupingNode()

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

class RuleReference(ASTNode):

    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.repeat_low = 1
        self.repeat_high = 1

    def walk(self, ancestors=None, rules=None):
        ancestors = ancestors or {}
        if self.rule_name != '_dictate':
            new_ancestors = ancestors + [self]
            try:
                rule = rules[self.rule_name]
            except KeyError:
                pass
            else:
                for child in rule.children:
                    yield from child.walk(new_ancestors, rules)
        yield {'node': self, 'ancestors': tuple(ancestors)}