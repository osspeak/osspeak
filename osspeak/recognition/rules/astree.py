import collections
import copy
import json
from recognition import lark_parser

class ASTNode:

    def walk(self):
        yield self

class Rule(ASTNode):

    def __init__(self):
        self.root = GroupingNode()

    def walk(self, ancestors=None, rules=None):
        yield self
        yield from self.root.walk()


class WordNode(ASTNode):

    def __init__(self, text):
        self.text = text
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_piece_substitute = None
        self.action = None

    @property
    def is_single(self):
        return self.repeat_low == 1 and self.repeat_high == 1

class GroupingNode(ASTNode):

    def __init__(self):
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_piece_substitute = None
        self.action = None
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
        self.action_piece_substitute = None
        self.action = None

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
    import lark.lexer
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
        try:
            high = int(child.children[1])
        except IndexError:
            high = None
    return low, high

def same_json(o1, o2):
    return json.dumps(o1, cls=RuleEncoder, sort_keys=True) == json.dumps(o2, cls=RuleEncoder, sort_keys=True)

class RuleEncoder(json.JSONEncoder):

    def default(self, o):
        d = o.__dict__.copy()
        d['type'] = o.__class__.__name__
        try:
            del d['action_piece_substitute']
        except KeyError:
            pass
        return d
