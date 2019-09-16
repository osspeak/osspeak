import lark.lexer
from recognition.actions.library import stdlib
from lib import keyboard
from recognition import lark_parser
import lark.tree
import types
import json

def parse_node(lark_ir):
    node_type = lark_parser.lark_node_type(lark_ir)
    value_ast = parse_map[node_type](lark_ir)
    return value_ast

def parse_expression_sequence(lark_ir):
    expressions = []
    last_ws = None
    for i, child in enumerate(lark_ir.children):
        node_type = lark_parser.lark_node_type(child)
        expr = parse_expr(child)
        expressions.append(expr)
    return ExpressionSequence(expressions)

def parse_expr(lark_ir):
    node_type = lark_parser.lark_node_type(lark_ir)
    if isinstance(lark_ir, lark.tree.Tree):
        value_ir = lark_ir.children[-1]
        value_ast = parse_node(value_ir)
        unary_ir = lark_parser.find_type(lark_ir, lark_parser.UNARY_OPERATOR)
        if unary_ir is not None:
            return UnaryOp('usub', value_ast)
    else:
        value_ast = parse_node(lark_ir)
    return value_ast

def parse_list(lark_ir):
    list_items = []
    for child in lark_ir.children:
        list_items.append(parse_node(child))
    return List(list_items)

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
    return BinOp(op, operand)

def parse_binop(lark_ir):
    op = 'add'
    left = parse_node(lark_ir.children[0])
    right = parse_node(lark_ir.children[2])
    return BinOp(op, left, right)

parse_map = {
    'literal': lambda x: Literal(''.join(str(s) for s in x.children)),
    'STRING_DOUBLE': lambda x: String(str(x)[1:-1]),
    'STRING_SINGLE': lambda x: String(str(x)[1:-1]),
    'list': parse_list,
    'expr': parse_expr,
    'attribute': parse_attribute,
    'call': parse_call,
    'keypress': parse_keypress,
    'binop': parse_binop,
    'variable': lambda x: Variable(int(x.children[0])),
    'NAME': lambda x: Name(str(x)),
    'INTEGER': lambda x: Integer(int(x)),
    'FLOAT': lambda x: Float(float(x)), 
    'WS': lambda x: Whitespace(str(x)),
    lark_parser.EXPR_SEQUENCE_SEPARATOR: lambda x: ExprSequenceSeparator(str(x)),
    lark_parser.ARGUMENT_REFERENCE: lambda x: ArgumentReference(str(x.children[0])),
    lark_parser.EXPR_SEQUENCE: parse_expression_sequence,
}

def evaluate_generator(gen):
    assert isinstance(gen, types.GeneratorType)
    last = None
    for node, item in exhaust_generator(gen):
        last = item
    return last

def exhaust_generator(gen):
    assert isinstance(gen, types.GeneratorType)
    for item in gen:
        if isinstance(item, types.GeneratorType):
            yield from exhaust_generator(item)
        else:
            yield item

class BaseActionNode:
    
    def evaluate(self, context):
        print(type(self))
        raise NotImplementedError

    def evaluate_lazy(self, context):
        yield self, self.evaluate(context)

class ExpressionSequence(BaseActionNode):

    def __init__(self, expressions):
        self.expressions = expressions

    def evaluate(self, context):
        evaluated_nodes = []
        last = None
        for i, expr in enumerate(self.expressions(context)):
            if isinstance(node, astree.Literal) and i > 1:
                second_previous, previous = self.expressions[i - 2:i]
                if isinstance(second_previous, astree.Literal) and isinstance(previous, astree.ExprSequenceSeparator):
                    last += previous.value
            result = expr.evaluate(context)
            if isinstance(last, str) and isinstance(result, str):
                last += result
            else:
                last = result
        return last

    def evaluate_lazy(self, context):
        for expr in self.expressions:
            yield from exhaust_generator(expr.evaluate_lazy(context))

class Literal(BaseActionNode):
    
    def __init__(self, value: str):
        self.value = value

    def evaluate(self, context):
        return self.value

class ArgumentReference(BaseActionNode):

    def __init__(self, value: str):
        self.value = value

    def evaluate(self, context):
        return context.argument_frames[-1][self.value]

class Whitespace(BaseActionNode):

    def __init__(self, value: str):
        self.value = value

    def evaluate(self, context):
        return self.value

class ExprSequenceSeparator(BaseActionNode):

    def __init__(self, value: str):
        self.value = value

    def evaluate(self, context):
        return None

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

    def __init__(self, value: float):
        self.value = value

    def evaluate(self, context):
        return self.value


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

    def prepare_call(self, context):
        kwarg_values = {}
        function_to_call = self.fn.evaluate(context)
        if function_to_call in stdlib.deferred_arguments_eval:
            arg_values = [context] + self.args
        else:
            arg_values = [arg.evaluate(context) for arg in self.args]
        return arg_values, kwarg_values, function_to_call

    def add_argument_frame(self, context, function_to_call, arg_values):
        frame = context.argument_frames[-1].copy()
        for i, arg_value in enumerate(arg_values):
            param = function_to_call.parameters[i]
            frame[param['name']] = arg_value
        context.argument_frames.append(frame)

    def evaluate(self, context):
        arg_values, kwarg_values, function_to_call = self.prepare_call(context)
        if isinstance(function_to_call, FunctionDefinition):
            self.add_argument_frame(context, function_to_call, arg_values)
            result = function_to_call.action.evaluate(context)
            context.argument_frames.pop()
            return result
        result = function_to_call(*arg_values, **kwarg_values)
        if isinstance(result, types.GeneratorType):
            return evaluate_generator(result)
        return result

    def evaluate_lazy(self, context):
        arg_values, kwarg_values, function_to_call = self.prepare_call(context)
        if isinstance(function_to_call, FunctionDefinition):
            self.add_argument_frame(context, function_to_call, arg_values)
            yield from function_to_call.action.evaluate_lazy(context)
            context.argument_frames.pop()
        else:
            result = function_to_call(*arg_values, **kwarg_values)
            if isinstance(result, types.GeneratorType):
                yield from exhaust_generator(result)
            else:
                yield self, result

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
    
class Variable(BaseActionNode):

    def __init__(self, value):
        self.value = value

    def get_actions(self, idx):
        pass

    def evaluate(self, context):
        index = self.value - 1 if self.value > 0 else self.value
        try:
            var_actions = context.variables[index]
        except IndexError:
            return
        last_result = None
        for action in var_actions:
            result = action.evaluate(context)
            if isinstance(last_result, str) and isinstance(result, str):
                last_result += result
            else:
                last_result = result
        return last_result

    def evaluate_lazy(self, context):
        index = self.value - 1 if self.value > 0 else self.value
        try:
            var_actions = context.variables[index]
        except IndexError:
            return
        for action in var_actions:
            yield from exhaust_generator(action.evaluate_lazy(context))

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
    return FunctionDefinition(name, params, action)

def to_json_string(action):
    return json.dumps(action, cls=SimpleJsonEncoder, sort_keys=True, indent=4)

class SimpleJsonEncoder(json.JSONEncoder):

    def default(self, o):
        d = o.__dict__.copy()
        d['type'] = o.__class__.__name__
        return d