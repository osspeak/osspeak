import lark.lexer
from recognition.actions import astree
from recognition import lark_parser
import lark.tree
import types
import json

operator_strings = {
    '+': 'add',
    '==': 'eq',
    '*': 'multiply',
    '**': 'pow',
    '-': 'subtract',
}

def compare_operators(a, b):
    precedence1, precedence2 = astree.operators[a]['precedence'], astree.operators[b]['precedence']
    if precedence1 > precedence2:
        return 'greater_than'
    if precedence1 < precedence2:
        return 'less_than'
    return 'equals'

def parse_node(lark_ir):
    node_type = lark_parser.lark_node_type(lark_ir)
    value_ast = parse_map[node_type](lark_ir)
    return value_ast

def parse_expression_sequence(lark_ir):
    expressions = []
    for i, child in enumerate(lark_ir.children):
        node_type = lark_parser.lark_node_type(child)
        expr = parse_expr(child)
        expressions.append(expr)
    return astree.ExpressionSequence(expressions)

def parse_expr(lark_ir):
    node_type = lark_parser.lark_node_type(lark_ir)
    if isinstance(lark_ir, lark.tree.Tree):
        value_ir = lark_ir.children[-1]
        value_ast = parse_node(value_ir)
        unary_ir = lark_parser.find_type(lark_ir, lark_parser.UNARY_OPERATOR)
        if unary_ir is not None:
            return astree.UnaryOp('usub', value_ast)
    else:
        value_ast = parse_node(lark_ir)
    return value_ast

def parse_list(lark_ir):
    list_items = []
    for child in lark_ir.children:
        list_items.append(parse_node(child))
    return astree.List(list_items)

def parse_loop(lark_ir):
    fn = astree.Name('loop')
    keys = [parse_node(x) for x in lark_ir.children]
    return astree.Call(fn, keys, {})

def parse_call(lark_ir):
    fn = parse_node(lark_ir.children[0])
    args_ir = lark_parser.find_type(lark_ir, lark_parser.ARG_LIST)
    args = [parse_node(x) for x in args_ir.children] if args_ir else []
    kwarg_list = lark_parser.find_type(lark_ir, lark_parser.KWARG_LIST)
    kwargs = {}
    if kwarg_list is not None:
        for kwarg_ir in kwarg_list.children:
            kwargs[str(kwarg_ir.children[0])] = parse_node(kwarg_ir.children[1])
    return astree.Call(fn, args, kwargs)

def parse_attribute(lark_ir):
    attribute_of = parse_node(lark_ir.children[0])
    name = str(lark_ir.children[1])
    return astree.Attribute(attribute_of, name)

def parse_keypress(lark_ir):
    fn = astree.Name('keypress')
    keys = [parse_node(x) for x in lark_ir.children]
    return astree.Call(fn, keys, {})

def parse_unaryop(lark_ir):
    op = 'usub'
    operand = parse_node(lark_ir.children[1])
    return astree.BinOp(op, operand)

def parse_binop(lark_ir):
    op_name = operator_strings[lark_ir.children[1]]
    left = parse_node(lark_ir.children[0])
    right = parse_node(lark_ir.children[2])
    node = astree.BinOp(op_name, left, right)
    if isinstance(left, astree.BinOp):
        if compare_operators(node.operator, node.left.operator) == 'greater_than':
            node.left, left.left, left.right = left.right, node, left.left
            return left
    if isinstance(right, astree.BinOp):
        if compare_operators(node.operator, node.right.operator) == 'greater_than':
            node.right, right.right, right.left = right.left, node, right.right
            return right
    return node

def parse_compare(lark_ir):
    left = parse_expr(lark_ir.children[0])
    ops = []
    comparators = []
    for i, child in enumerate(lark_ir.children[1:], start=1):
        if i % 2 == 1:
            ops.append(str(child))
        else:
            comparators.append(parse_expr(child))
    return astree.Compare(left, ops, comparators)

def parse_index(lark_ir):
    index_of = parse_node(lark_ir.children[0])
    index = parse_node(lark_ir.children[1])
    return astree.Index(index_of, index)

def parse_slice(lark_ir):
    slice_pieces = [None, None, None]
    i = 0
    slice_of = parse_node(lark_ir.children[0])
    for child in lark_ir.children[1:]:
        if lark_parser.lark_node_type(child) == lark_parser.SLICE_SEPARATOR:
            i += 1
        else:
            slice_pieces[i] = parse_node(child)
    start, stop, step = slice_pieces
    return astree.Slice(slice_of, start, stop, step)

parse_map = {
    'literal': lambda x: astree.Literal(''.join(str(s) for s in x.children)),
    'STRING_DOUBLE': lambda x: astree.String(str(x)[1:-1]),
    'STRING_SINGLE': lambda x: astree.String(str(x)[1:-1]),
    'compare': parse_compare,
    'list': parse_list,
    'loop': parse_loop,
    'expr': parse_expr,
    'attribute': parse_attribute,
    'call': parse_call,
    'keypress': parse_keypress,
    'left_to_right': parse_binop,
    'right_to_left': parse_binop,
    'variable': lambda x: astree.Variable(int(x.children[0])),
    'NAME': lambda x: astree.Name(str(x)),
    'INTEGER': lambda x: astree.Integer(int(x)),
    'FLOAT': lambda x: astree.Float(float(x)),
    'index': parse_index,
    'slice': parse_slice,
    lark_parser.EXPR_SEQUENCE_SEPARATOR: lambda x: astree.ExprSequenceSeparator(str(x)),
    lark_parser.ARGUMENT_REFERENCE: lambda x: astree.ArgumentReference(str(x.children[0])),
    lark_parser.EXPR_SEQUENCE: parse_expression_sequence,
}

def action_root_from_text(text):
    lark_ir = lark_parser.parse_action(text)
    return action_from_lark_ir(lark_ir, text)

def action_from_lark_ir(root_lark_ir, text):
    return parse_node(root_lark_ir)

def function_definition_from_lark_ir(lark_ir):
    name = str(lark_ir.children[0])
    action_ir = lark_ir.children[-1]
    positional_parameters = lark_parser.find_type(lark_ir, 'positional_parameters')
    params = []
    if positional_parameters:
        for param_ir in positional_parameters.children:
            params.append({'name': str(param_ir)})
    action = action_from_lark_ir(action_ir, '')
    return astree.FunctionDefinition(name, params, action)

def to_json_string(action):
    return json.dumps(action, cls=SimpleJsonEncoder, sort_keys=True, indent=4)

class SimpleJsonEncoder(json.JSONEncoder):

    def default(self, o):
        d = o.__dict__.copy()
        d['type'] = o.__class__.__name__
        return d