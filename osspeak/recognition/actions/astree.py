import lark.lexer
from recognition import lark_parser
import lark.tree
import json


def parse_expr(lark_ir):
    print(lark_ir)
    value_ir = lark_ir.children[-1]
    type_attr = 'data' if isinstance(value_ir, lark.tree.Tree) else 'type'
    node_type = getattr(value_ir, type_attr)
    value_ast = parse_map[node_type](value_ir)
    unary_ir = find_type(lark_ir, lark_parser.UNARY_OPERATOR)
    if unary_ir is not None:
        return UnaryOp('usub', value_ast)
    return value_ast

def parse_list(lark_ir):
    list_items = []
    for child in lark_ir.children:
        list_items.append(parse_expr(child))
    return List(list_items)

def parse_index(lark_ir):
    index_of = parse_expr(lark_ir.children[0])
    index_key = parse_expr(lark_ir.children[1])
    return Index(index_of, index_key)

def parse_call(lark_ir):
    fn = parse_expr(lark_ir.children[0])
    try:
        args_ir = list(lark_ir.find_data(lark_parser.ARG_LIST))[0]
    except IndexError:
        args = []
    else:
        args = [parse_expr(x) for x in args_ir.children]
    try:
        kwargs_ir = list(lark_ir.find_data(lark_parser.ARG_LIST))[0]
    except IndexError:
        kwargs_ir = []
    kwargs = {}
    return Call(fn, args, kwargs)

def parse_attribute(lark_ir):
    attribute_of = parse_expr(lark_ir.children[0])
    name = str(lark_ir.children[1])
    return Attribute(attribute_of, name)

def parse_keypress(lark_ir):
    fn = Name('keypress')
    keys = [parse_expr(x) for x in lark_ir.children]
    return Call(fn, keys, {})

def parse_unaryop(lark_ir):
    op = 'usub'
    operand = parse_expr(lark_ir.children[1])
    # right = parse_expr(lark_ir.children[2])
    return BinOp(op, operand)

def parse_binop(lark_ir):
    op = 'add'
    left = parse_expr(lark_ir.children[0])
    right = parse_expr(lark_ir.children[2])
    return BinOp(op, left, right)

parse_map = {
    'literal': lambda x: String(''.join(str(s) for s in x.children)),
    'STRING_DOUBLE': lambda x: String(str(x)[1:-1]),
    'STRING_SINGLE': lambda x: String(str(x)[1:-1]),
    'list': parse_list,
    'index': parse_index,
    'attribute': parse_attribute,
    'call': parse_call,
    'keypress': parse_keypress,
    'binop': parse_binop,
    'variable': lambda x: Name(str(x.children[0])),
    'NAME': lambda x: Name(str(x)),
    'INTEGER': lambda x: Integer(int(x)),
    'FLOAT': lambda x: Float(float(x))
}

class BaseActionNode:
    
    def evaluate(self):
        raise NotImplementedError

class Action(BaseActionNode):

    def __init__(self, expressions):
        self.expressions = expressions

class String(BaseActionNode):

    def __init__(self, value: str):
        self.value = value

    def evaluate(self):
        return self.value

class Integer(BaseActionNode):

    def __init__(self, value: int):
        self.value = value

class Float(BaseActionNode):

    def __init__(self, value: int):
        self.value = value

class UnaryOp(BaseActionNode):

    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand

class BinOp(BaseActionNode):

    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

class List(BaseActionNode):

    def __init__(self, items):
        self.items = items

class Index(BaseActionNode):

    def __init__(self, index_of, index_key):
        self.index_of = index_of
        self.index_key = index_key

class Attribute(BaseActionNode):

    def __init__(self, attribute_of, name):
        self.attribute_of = attribute_of
        self.name = name

class Call(BaseActionNode):

    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

class Name(BaseActionNode):

    def __init__(self, value):
        self.value = value

class Variable(BaseActionNode):

    def __init__(self, value):
        self.value = value

def action_from_lark_ir(root_lark_ir, text):
    expressions = []
    for child in root_lark_ir.children:
        expr = parse_expr(child)
        expressions.append(expr)
    return Action(expressions)

def find_type(lark_tree, _type):
    for child in lark_tree.children:
        child_type_attr = 'data' if isinstance(child, lark.tree.Tree) else 'type'
        child_type = getattr(child, child_type_attr)
        if child_type == _type:
            return child

def to_json_string(action):
    return json.dumps(action, cls=ActionEncoder, sort_keys=True, indent=4)

class ActionEncoder(json.JSONEncoder):

    def default(self, o):
        d = o.__dict__.copy()
        d['type'] = o.__class__.__name__
        # try:
        #     del d['action_piece_substitute']
        # except KeyError:
        #     pass
        return d