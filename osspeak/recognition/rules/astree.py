import collections
import copy
from recognition import lark_parser

class ASTNode:

    def walk(self):
        yield self

    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        return id(self)

class Rule(ASTNode):

    def __init__(self, name=None, text=''):
        self.name = name
        self.text = text
        self.root = GroupingNode()

    def walk(self, ancestors=None, rules=None):
        yield self
        yield from self.root.walk()

    def __eq__(self, other):
        return self.root == other.root

    def __hash__(self):
        return id(self)


class WordNode(ASTNode):

    def __init__(self, text):
        self.text = text
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_piece_substitute = None

    @property
    def is_single(self):
        return self.repeat_low == 1 and self.repeat_high == 1

    def __eq__(self, other):
        return check_equal(self, other, ('repeat_low', 'repeat_high'))

    def __hash__(self):
        return id(self)


class GroupingNode(ASTNode):

    def __init__(self):
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_piece_substitute = None
        self.sequences = []

    def walk(self):
        yield self
        for seq in self.sequences:
            for node in seq:
                yield from node.walk()

    def __eq__(self, other):
        return check_equal(self, other, ('repeat_low', 'repeat_high', 'sequences'))

    def __hash__(self):
        return id(self)

class RuleReference(ASTNode):

    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_piece_substitute = None

    def __eq__(self, other):
        return check_equal(self, other, ('repeat_low', 'repeat_high', 'rule_name'))

    def __hash__(self):
        return id(self)

def check_equal(obj1, obj2, attrs):
    if type(obj1) is not type(obj2):
        return False
    equal, not_equal = compare_attributes(obj1, obj2, attrs)
    if not_equal:
        return False
    return True

def compare_attributes(o1, o2, attrs):
    equal = []
    not_equal = []
    for attr in attrs:
        if getattr(o1, attr) == getattr(o2, attr):
            equal.append(attr)
        else:
            not_equal.append(attr)
    return equal, not_equal

def rule_from_ast(lark_ast):
    rule = Rule()
    rule.root = grouping_from_choice_items(lark_ast.children[0])
    return rule

def grouping_from_choice_items(ast):
    grouping = GroupingNode()
    for ast_sequence in ast.children:
        sequence = sequence_from_ast_sequence(ast_sequence)
        grouping.sequences.append(sequence)
    return grouping

def sequence_from_ast_sequence(ast):
    seq = []
    for utterance_piece in ast.children:
        seq.append(node_from_utterance_piece(utterance_piece))
    return seq

def node_from_utterance_piece(ast):
    wrapped_ast = ast.children[0]
    node = None
    if wrapped_ast.data == lark_parser.UTTERANCE_WORD:
        word = str(wrapped_ast.children[0])
        node = WordNode(word)
    elif wrapped_ast.data == lark_parser.UTTERANCE_CHOICES:
        choice_items = wrapped_ast.children[0]
        node = grouping_from_choice_items(choice_items)
    elif wrapped_ast.data == lark_parser.UTTERANCE_REFERENCE:
        ref = wrapped_ast.children[0]
        ref_name = ref.children[0]
        node = RuleReference(ref_name)
    rep = list(ast.find_data(lark_parser.UTTERANCE_REPETITION))
    if rep:
        node.repeat_low, node.repeat_high = parse_repetition(rep[0])
    return node

def parse_repetition(ast):
    import lark.lexer
    child = ast.children[0]
    low, high = 1, 1
    if isinstance(child, lark.lexer.Token) and child.type == lark_parser.ZERO_OR_POSITIVE_INT:
        low, high = int(child), int(child)
    elif child.data == lark_parser.UTTERANCE_RANGE:
        low = int(child.children[0])
        high = int(child.children[1])
    return low, high
