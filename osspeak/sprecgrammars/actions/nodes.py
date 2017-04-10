import re
import types
import itertools
import functools

from sprecgrammars.functions import library
from platforms import api

class Action:

    def __init__(self):
        # what follows an underscore, ie {left_2_down}
        self.modifiers = []
        self.slices = []

    def evaluate(self, variables):
        raise NotImplementedError

    def add(self, *a, **k):
        raise NotImplementedError

    def error(self, msg):
        raise RuntimeError(msg)


    def apply_slices(self, val, variables, arguments):
        for action_slice in self.slices:
            val = action_slice.apply(val, variables, arguments)
        return val


class RootAction(Action):

    def __init__(self):
        super().__init__()
        self.children = []
        self.raw_text = None

    def add(self, child):
        self.children.append(child)

    def evaluate(self, variables, arguments=None, type_result=False, result_state=None):
        result = ''
        return_last_evaluation = False
        evaluations = []
        for child in self.children:
            child_result = child.evaluate(variables, arguments=arguments, type_result=type_result, result_state=result_state)
            evaluations.append(child_result)
            if isinstance(child_result, (str, int, float)):
                result += str(child_result)
            elif result is None:
                continue
            else:
                return_last_evaluation = True
        return evaluations[-1] if return_last_evaluation else result

    def perform(self, variables, arguments=None):
        result_state = {'store in history': True}
        self.evaluate(variables, arguments, type_result=True, result_state=result_state)
        return result_state

class LiteralKeysAction(Action):

    # $3, $-2 etc.
    var_pattern = re.compile(r'\$-?\d+')
    
    def __init__(self, text, is_template=False):
        super().__init__()
        self.text = text
        self.is_template = is_template

    def evaluate_text(self, variables, arguments, result_state):
        if not self.is_template:
            text = self.text
        else:
            matchfunc = functools.partial(self.var_replace, variables, arguments, result_state)
            text = re.sub(self.var_pattern, matchfunc, self.text)
        text = self.apply_slices(text, variables, arguments)
        return text

    def var_replace(self, variables, arguments, matchobj, result_state):
        grouping_start, grouping_end = matchobj.regs[0]
        match_index = int(matchobj.string[grouping_start + 1: grouping_end])
        if match_index > 0:
            match_index -= 1
        try:
            var = variables[match_index]
        except IndexError:
            return ''
        return var.evaluate(variables, arguments, result_state=result_state)

    def evaluate(self, variables, arguments=None, type_result=False, result_state=None):
        result = self.evaluate_text(variables, arguments, result_state)
        if type_result:
            api.type_line(result)
        return result

class FunctionCall(Action):

    def __init__(self, func_name):
        super().__init__()
        self.arguments = []
        self.func_name = func_name
        self.definition = None

    def add(self, node):
        self.arguments.append(node)

    def get_arguments(self, variables, arguments, result_state=None):
        args = {}
        # use default action for any arg not passed by user
        for param, arg in itertools.zip_longest(self.definition.parameters, self.arguments):
            action = param.default_action if arg is None else arg
            args[param.name] = action.evaluate(variables, arguments, result_state=result_state)
        return args

    def evaluate(self, variables, arguments=None, type_result=False, result_state=None):
        from sprecgrammars.api import action
        # builtin functions
        if isinstance(self.definition, types.FunctionType):
            if self.func_name in library.builtin_functions_custom_evaluation:
                args = [self, variables, arguments, type_result, result_state]
                # gets taken care of in function call
                type_result = False
            else:
                args = [a.evaluate(variables, arguments, result_state=result_state) for a in self.arguments]
            result = self.definition(*args)
            if self.func_name == 'history.last':
                result_state['store in history'] = False
        # user defined functions
        else:
            args = self.get_arguments(variables, arguments, result_state=result_state)
            result = self.definition.action.evaluate(variables, args, type_result=type_result, result_state=result_state)
            type_result = False
        if type_result:
            api.type_line(result)
        return self.apply_slices(result, variables, arguments)

class KeySequence(Action):

    def __init__(self):
        super().__init__()
        self.keys = []

    def add(self, node):
        self.keys.append(node)

    def evaluate(self, variables, arguments=None, type_result=False, result_state=None):
        keys = [node.evaluate(variables, arguments, result_state=result_state) for node in self.keys]
        result = [[keys]]
        if type_result:
            api.type_line(result)
        return result

class PositionalVariable(Action):

    def __init__(self, pos):
        super().__init__()
        self.pos = pos

    def evaluate(self, variables, arguments=None, type_result=False, result_state=None):
        pos = self.pos - 1 if self.pos > 0 else self.pos
        var = variables[pos]
        result = var.evaluate(variables, arguments, type_result=type_result, result_state=result_state)
        sliced_result = self.apply_slices(result, variables, arguments)
        return sliced_result

class WhitespaceNode(Action):

    def __init__(self, text):
        super().__init__()
        self.text = text

    def evaluate(self, variables, arguments=None, type_result=False, result_state=None):
        pass

class NumberNode(Action):

    def __init__(self, number):
        super().__init__()
        self.number = number

    def evaluate(self, variables, arguments=None, type_result=False, result_state=None):
        if type_result:
            api.type_line(self.number)
        return self.number

class Argument(Action):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def evaluate(self, variables, arguments=None, type_result=False, result_state=None):
        arguments = {} if arguments is None else arguments
        result = arguments.get(self.name, '')
        result = self.apply_slices(result, variables, arguments)
        if type_result:
            api.type_line(result)
        return result