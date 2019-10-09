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
        self.action_substitute = None

    @property
    def is_single(self):
        return self.repeat_low == 1 and self.repeat_high == 1

class GroupingNode(ASTNode):

    def __init__(self):
        self.repeat_low = 1
        self.repeat_high = 1
        self.action_substitute = None
        self.ignore_ambiguities = False
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
        self.ignore_ambiguities = False

def utterance_from_lark_ir(lark_ir):
    rule = Rule()
    rule.root = grouping_from_choice_items(lark_ir.children[0])
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

def node_from_utterance_piece(lark_ir):
    import lark.lexer
    import recognition.actions.astree_constructor
    wrapped_node = lark_ir.children[0]
    wrapped_type = lark_parser.lark_node_type(wrapped_node)
    ignore_ambiguities = lark_parser.find_type(wrapped_node, lark_parser.IGNORE_AMBIGUITIES)
    if wrapped_type == lark_parser.UTTERANCE_WORD:
        word_text = str(wrapped_node)
        node = WordNode(word_text)
    elif wrapped_type == lark_parser.UTTERANCE_CHOICES:
        choice_items = lark_parser.find_type(wrapped_node, lark_parser.UTTERANCE_CHOICE_ITEMS)
        node = grouping_from_choice_items(choice_items)
    elif wrapped_type == lark_parser.UTTERANCE_CHOICES_OPTIONAL:
        choice_items = lark_parser.find_type(wrapped_node, lark_parser.UTTERANCE_CHOICE_ITEMS)
        node = grouping_from_choice_items(choice_items)
        node.repeat_low, node.repeat_high = 0, 1
    elif wrapped_type == lark_parser.UTTERANCE_REFERENCE:
        ref = lark_parser.find_type(wrapped_node, lark_parser.UTTERANCE_NAME)
        ref_name = ref.children[0]
        node = RuleReference(ref_name)
    else:
        raise ValueError(f'Unrecognized utterance piece type: {wrapped_type}')
    if ignore_ambiguities:
        node.ignore_ambiguities = True
    rep = lark_parser.find_type(lark_ir, lark_parser.UTTERANCE_REPETITION)
    if rep:
        node.repeat_low, node.repeat_high = parse_repetition(rep)
    substitute = lark_parser.find_type(lark_ir, lark_parser.ACTION_SUBSTITUTE)
    if substitute:
        node.action_substitute = recognition.actions.astree_constructor.action_from_lark_ir(substitute.children[0], 'foo')
    return node

def parse_repetition(lark_ir):
    if lark_ir.children[0] == '*':
        return 0, None
    if lark_ir.children[0] == '?':
        return 0, 1
    if lark_ir.children[0] == '+':
        return 1, None
    import lark.lexer
    child = lark_ir.children[1]
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
        return d
