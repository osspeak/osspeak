import lark.lexer
from lib import keyboard
from recognition import lark_parser
import lark.tree
import types
import json

def parse_node(lark_ir):
    type_attr = 'data' if isinstance(lark_ir, lark.tree.Tree) else 'type'
    node_type = getattr(lark_ir, type_attr)
    value_ast = parse_map[node_type](lark_ir)
    return value_ast

def parse_expr(lark_ir):
    value_ir = lark_ir.children[-1]
    value_ast = parse_node(value_ir)
    unary_ir = lark_parser.find_type(lark_ir, lark_parser.UNARY_OPERATOR)
    if unary_ir is not None:
        return UnaryOp('usub', value_ast)
    return value_ast

def parse_list(lark_ir):
    list_items = []
    for child in lark_ir.children:
        list_items.append(parse_node(child))
    return List(list_items)

def parse_index(lark_ir):
    index_of = parse_node(lark_ir.children[0])
    index_key = parse_node(lark_ir.children[1])
    return Index(index_of, index_key)

def parse_call(lark_ir):
    fn = parse_node(lark_ir.children[0])
    args_ir = lark_parser.find_type(lark_ir, lark_parser.ARG_LIST)
    args = [parse_node(x) for x in args_ir.children] if args_ir else []
    kwargs_ir = lark_parser.find_type(lark_ir, lark_parser.KWARG_LIST) or {}
    kwargs = {}
    return Call(fn, args, kwargs)

def parse_attribute(lark_ir):
    attribute_of = parse_node(lark_ir.children[0])
    name = str(lark_ir.children[1])
    return Attribute(attribute_of, name)

def parse_keypress(lark_ir):
    fn = Name('keypress')
    keys = [parse_node(x) for x in lark_ir.children]
    return Call(fn, keys, {})

def parse_unaryop(lark_ir):
    op = 'usub'
    operand = parse_node(lark_ir.children[1])
    # right = parse_node(lark_ir.children[2])
    return BinOp(op, operand)

def parse_binop(lark_ir):
    op = 'add'
    left = parse_node(lark_ir.children[0])
    right = parse_node(lark_ir.children[2])
    return BinOp(op, left, right)

parse_map = {
    'literal': lambda x: String(''.join(str(s) for s in x.children)),
    'STRING_DOUBLE': lambda x: String(str(x)[1:-1]),
    'STRING_SINGLE': lambda x: String(str(x)[1:-1]),
    'list': parse_list,
    'expr': parse_expr,
    'index': parse_index,
    'attribute': parse_attribute,
    'call': parse_call,
    'keypress': parse_keypress,
    'binop': parse_binop,
    'variable': lambda x: Variable(int(x.children[0])),
    'NAME': lambda x: Name(str(x)),
    'INTEGER': lambda x: Integer(int(x)),
    'FLOAT': lambda x: Float(float(x))
}

class BaseActionNode:
    
    def evaluate(self, context):
        print(type(self))
        raise NotImplementedError

class Action(BaseActionNode):

    def __init__(self, expressions):
        self.expressions = expressions

    def perform(self, context):
        gen = self.evaluate(context)
        for result in self.exhaust_generator(gen):
            if isinstance(result, (str, float, int)):
                keyboard.write(str(result), delay=.05)

    def exhaust_generator(self, gen):
        for item in gen:
            if isinstance(item, types.GeneratorType):
                yield from self.exhaust_generator(item)
            else:
                yield item

    def evaluate(self, context):
        for expr in self.expressions:
            result = expr.evaluate(context)
            yield result

class String(BaseActionNode):

    def __init__(self, value: str):
        self.value = value

    def evaluate(self, context):
        return self.value

class Integer(BaseActionNode):

    def __init__(self, value: int):
        self.value = value

    def evaluate(self, context):
        return self.value

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

    def evaluate(self, context):
        return self.index_of.evaluate(context)[self.index_key.evaluate(context)]

class Attribute(BaseActionNode):

    def __init__(self, attribute_of, name):
        self.attribute_of = attribute_of
        self.name = name

    def evaluate(self, context):
        attribute_of_value = self.attribute_of.evaluate(context)
        return getattr(attribute_of_value, self.name)

class Call(BaseActionNode):

    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def evaluate(self, context):
        arg_values = [arg.evaluate(context) for arg in self.args]
        kwarg_values = {}
        function_to_call = self.fn.evaluate(context)
        if isinstance(function_to_call, FunctionDefinition):
            return function_to_call(context, *arg_values, **kwarg_values)
        return function_to_call(*arg_values, **kwarg_values)

class Name(BaseActionNode):

    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return context.namespace[self.value]

class FunctionDefinition:

    def __init__(self, name: str, parameters, action):
        self.name = name
        self.parameters = parameters
        self.action = action
    
    def __call__(self, context, *args, **kwargs):
        print(self.action.evaluate(context))
        return self.action.evaluate(context)

class Variable(BaseActionNode):

    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        index = self.value - 1 if self.value > 0 else self.value
        try:
            var_actions = context.variables[index]
        except IndexError:
            return
        last_result = None
        for action in var_actions:
            for result in action.evaluate(context):
                last_result = result
        return last_result

def action_from_text(text):
    lark_ir = lark_parser.parse_action(text)
    return action_from_lark_ir(lark_ir, text)

def action_from_lark_ir(root_lark_ir, text):
    expressions = []
    for child in root_lark_ir.children:
        expr = parse_node(child)
        expressions.append(expr)
    return Action(expressions)

def function_definition_from_lark_ir(lark_ir):
    name = str(lark_ir.children[0])
    action_ir = lark_parser.find_type(lark_ir, 'action')
    positional_parameters = lark_parser.find_type(lark_ir, 'positional_parameters')
    params = []
    if positional_parameters:
        for param_ir in positional_parameters.children:
            params.append({'name': str(param_ir)})
    action = action_from_lark_ir(action_ir, '')
    return FunctionDefinition(name, params, action)

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