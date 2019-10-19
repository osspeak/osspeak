import lark.lexer
from recognition.actions.library import stdlib
from lib import keyboard
from recognition import lark_parser
import lark.tree
import types
import json
import operator

operators = {
    'multiply': {'precedence': 11, 'function': operator.mul},
    'divide': {'precedence': 11, 'function': operator.truediv},
    'add': {'precedence': 10, 'function': operator.add},
    'subtract': {'precedence': 10, 'function': operator.sub},
    'eq': {'precedence': 5, 'function': operator.eq},
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
        for i, expr in enumerate(self.expressions):
            if isinstance(expr, Literal) and i > 1:
                second_previous, previous = self.expressions[i - 2:i]
                if isinstance(second_previous, Literal) and isinstance(previous, ExprSequenceSeparator):
                    last += previous.value
            result = expr.evaluate(context)
            if isinstance(last, str) and isinstance(result, str):
                last += result
            elif result is not None:
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

    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self, context):
        left = self.left.evaluate(context)
        right = self.right.evaluate(context)
        return operators[self.operator]['function'](left, right)
        if self.operator == 'add':
            return left + right
        if self.operator == 'multiply':
            return left * right
        raise NotImplementedError

class Compare(BaseActionNode):

    def __init__(self, left, ops, comparators):
        self.left = left
        self.ops = ops
        self.comparators = comparators

class List(BaseActionNode):

    def __init__(self, items):
        self.items = items

    def evaluate(self, context):
        return [x.evaluate(context) for x in self.items]

class Attribute(BaseActionNode):

    def __init__(self, attribute_of, name):
        self.attribute_of = attribute_of
        self.name = name

    def evaluate(self, context):
        attribute_of_value = self.attribute_of.evaluate(context)
        return getattr(attribute_of_value, self.name)

class Index(BaseActionNode):

    def __init__(self, index_of, index):
        self.index_of = index_of
        self.index = index

    def evaluate(self, context):
        index_of_value = self.index_of.evaluate(context)
        index = self.index.evaluate(context)
        return index_of_value[index]

class Slice(BaseActionNode):

    def __init__(self, slice_of, start, stop, step):
        self.slice_of = slice_of
        self.start = start
        self.stop = stop
        self.step = step

    def evaluate(self, context):
        slice_of_value = self.slice_of.evaluate(context)
        start = None if self.start is None else self.start.evaluate(context)
        stop = None if self.stop is None else self.stop.evaluate(context)
        step = None if self.step is None else self.step.evaluate(context)
        return slice_of_value[start:stop:step]

class Call(BaseActionNode):

    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def prepare_call(self, context):
        kwarg_values = {k: v.evaluate(context) for k, v in self.kwargs.items()}
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
            elif result is not None:
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