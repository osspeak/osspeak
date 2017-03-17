import re
import types
import itertools
import functools

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

    def apply_modifiers(self, variables):
        applied_modifiers = {}
        evaluated_modifiers = [action.evaluate(variables) for action in self.modifiers]
        for modifier in evaluated_modifiers:
            if str(modifier).isdigit():
                if 'repeat' in applied_modifiers:
                    self.error('multiple nums')
                applied_modifiers['repeat'] = int(modifier)
            else:
                if 'direction' in applied_modifiers:
                    self.error('multiple nums')
                applied_modifiers['direction'] = modifier
        return applied_modifiers

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

    def evaluate(self, variables, arguments=None, type_result=False):
        result = ''
        for child in self.children:
            child_result = child.evaluate(variables, arguments=arguments, type_result=type_result)
            if isinstance(child_result, str):
                result += child_result
        return result

    def perform(self, variables, arguments=None):
        self.evaluate(variables, arguments, type_result=True)

class LiteralKeysAction(Action):

    # $3, $-2 etc.
    var_pattern = re.compile(r'\$-?\d+')
    
    def __init__(self, text, is_template=False):
        super().__init__()
        self.text = text
        self.is_template = is_template

    def evaluate_text(self, variables, arguments):
        if not self.is_template:
            text = self.text
        else:
            matchfunc = functools.partial(self.var_replace, variables, arguments)
            text = re.sub(self.var_pattern, matchfunc, self.text)
        text = self.apply_slices(text, variables, arguments)
        modifiers = self.apply_modifiers(variables)
        return text * modifiers.get('repeat', 1)

    def var_replace(self, variables, arguments, matchobj):
        grouping_start, grouping_end = matchobj.regs[0]
        match_index = int(matchobj.string[grouping_start + 1: grouping_end])
        if match_index > 0:
            match_index -= 1
        try:
            var = variables[match_index]
        except IndexError:
            return ''
        return var.evaluate(variables, arguments)

    def evaluate(self, variables, arguments=None, type_result=False):
        result = self.evaluate_text(variables, arguments)
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

    def get_arguments(self, variables, arguments):
        args = {}
        # use default action for any arg not passed by user
        for param, arg in itertools.zip_longest(self.definition.parameters, self.arguments):
            action = param.default_action if arg is None else arg
            args[param.name] = action.evaluate(variables, arguments)
        return args

    def evaluate(self, variables, arguments=None, type_result=False):
        from sprecgrammars.api import action
        # builtin functions
        if isinstance(self.definition, types.FunctionType):
            args = [a.evaluate(variables, arguments) for a in self.arguments]
            result = self.definition(*args)
        # user defined functions
        else:
            args = self.get_arguments(variables, arguments)
            result = self.definition.action.evaluate(variables, args, type_result=type_result)
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

    def evaluate(self, variables, arguments=None, type_result=False):
        modifiers = self.apply_modifiers(variables)
        keys = [node.evaluate(variables, arguments) for node in self.keys]
        result = [[keys for i in range(modifiers.get('repeat', 1))]]
        if type_result:
            api.type_line(result)

class PositionalVariable(Action):

    def __init__(self, pos):
        super().__init__()
        self.pos = pos

    def evaluate(self, variables, arguments=None, type_result=False):
        pos = self.pos - 1 if self.pos > 0 else self.pos
        var = variables[pos]
        modifiers = self.apply_modifiers(variables)
        result = var.evaluate(variables, arguments, type_result=type_result)
        try:
            result = result * modifiers.get('repeat', 1)
        except TypeError:
            pass
        return self.apply_slices(result, variables, arguments)

class WhitespaceNode(Action):

    def __init__(self, text):
        super().__init__()
        self.text = text

    def evaluate(self, variables, arguments=None, type_result=False):
        pass

class NumberNode(Action):

    def __init__(self, number):
        super().__init__()
        self.number = number

    def evaluate(self, variables, arguments=None, type_result=False):
        modifiers = self.apply_modifiers(variables)
        if type_result:
            api.type_line(self.number)
        return self.number

class Argument(Action):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def evaluate(self, variables, arguments=None, type_result=False):
        arguments = {} if arguments is None else arguments
        result = arguments.get(self.name, '')
        if type_result:
            api.type_line(result)
        return result