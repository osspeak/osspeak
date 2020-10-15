from recognition.actions import astree
from recognition import lark_parser
import lark.tree
import types
import json
import operator

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

def parse_unary(lark_ir):
    value_ir = lark_ir.children[-1]
    value_ast = parse_node(value_ir)
    unary_ir = lark_ir.children[0]
    if unary_ir is not None:
        if unary_ir == '+':
            op = 'positive'
        elif unary_ir == '-':
            op = 'negative'
        else:
            raise ValueError()
        return astree.UnaryOp(op, value_ast)
    return value_ast

def parse_expr(lark_ir):
    node_type = lark_parser.lark_node_type(lark_ir)
    if isinstance(lark_ir, lark.tree.Tree):
        value_ir = lark_ir.children[-1]
        value_ast = parse_node(value_ir)
    else:
        value_ast = parse_node(lark_ir)
    return value_ast

def left_to_right(lark_ir, default_operation=None, operator_map=None):
    operation_class = default_operation 
    left = parse_node(lark_ir.children[0])
    for child in lark_ir.children[1:]:
        if isinstance(child, lark.lexer.Token):
            operation_class = operator_map[child]
        else:
            right = parse_node(child)
            left = operation_class(left, right)
    return left

def parse_exponent(lark_ir):
    right = parse_node(lark_ir.children[-1])
    for child in reversed(lark_ir.children[:-1]):
        left = parse_node(child)
        right = astree.Exponent(left, right)
    return right

def parse_compare(lark_ir):
    if len(lark_ir.children) == 1:
        return parse_node(lark_ir.children[0])
    left = parse_node(lark_ir.children[0])
    ops = []
    comparators = []
    for i, child in enumerate(lark_ir.children[1:]):
        if i % 2 == 0:
            ops.append(str(child))
        else:
            comparators.append(parse_node(child))
    return astree.Compare(left, ops, comparators)

def parse_or(lark_ir):
    return left_to_right(lark_ir, default_operation=astree.Or)

def parse_and(lark_ir):
    return left_to_right(lark_ir, default_operation=astree.And)

def parse_not(lark_ir):
    parsed_child = parse_node(lark_ir.children[-1])
    if lark_ir.children[0] is not None:
        return astree.UnaryOp('not', parsed_child)
    return parsed_child

def parse_additive(lark_ir):
    operator_map = {'+': astree.Add, '-': astree.Subtract}
    return left_to_right(lark_ir, operator_map=operator_map)

def parse_multiplicative(lark_ir):
    operator_map = {'*': astree.Multiply, '/': astree.Divide}
    return left_to_right(lark_ir, operator_map=operator_map)

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
    keys = parse_node(lark_ir.children[0])
    return astree.KeySequence(keys)

def parse_index(lark_ir):
    index_of = parse_node(lark_ir.children[0])
    index = parse_node(lark_ir.children[1])
    return astree.Index(index_of, index)

def parse_slice(lark_ir):
    slice_pieces = [None, None, None]
    i = 0
    slice_of = parse_node(lark_ir.children[0])
    for child in lark_ir.children[1:]:
        if child is None or lark_parser.lark_node_type(child) == lark_parser.SLICE_SEPARATOR:
            i += 1
        else:
            slice_pieces[i] = parse_node(child)
    start, stop, step = slice_pieces
    return astree.Slice(slice_of, start, stop, step)

parse_map = {
    'literal': lambda x: astree.Literal(''.join(str(s) for s in x.children)),
    'STRING_DOUBLE': lambda x: astree.String(str(x)[1:-1].replace('\\\\', '\\')),
    'STRING_SINGLE': lambda x: astree.String(str(x)[1:-1].replace('\\\\', '\\')),
    'REGEX': lambda x: astree.RegularExpression(str(x)[1:-1]),
    'list': parse_list,
    'loop': parse_loop,
    'expr': parse_expr,
    'attribute': parse_attribute,
    'call': parse_call,
    'keypress': parse_keypress,
    'variable': lambda x: astree.Variable(int(x.children[0])),
    'NAME': lambda x: astree.Name(str(x)),
    'INTEGER': lambda x: astree.Integer(int(x)),
    'ZERO_OR_POSITIVE_INTEGER': lambda x: astree.Integer(int(x)),
    'ZERO_OR_POSITIVE_FLOAT': lambda x: astree.Float(float(x)),
    'index': parse_index,
    'slice': parse_slice,
    lark_parser.EXPR_SEQUENCE_SEPARATOR: lambda x: astree.ExprSequenceSeparator(str(x)),
    lark_parser.ARGUMENT_REFERENCE: lambda x: astree.ArgumentReference(str(x.children[0])),
    lark_parser.EXPR_SEQUENCE: parse_expression_sequence,
    'compare': parse_compare,
    'or': parse_or,
    'and': parse_and,
    'not': parse_not,
    'additive': parse_additive,
    'multiplicative': parse_multiplicative,
    'unary': parse_unary,
    'exponent': parse_exponent,
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