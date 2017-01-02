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

    def perform(self, variables):
        raise NotImplementedError

    def add(self, *a, **k):
        raise NotImplementedError

    def error(self, msg):
        raise RuntimeError(msg)

    def apply_modifiers(self, variables):
        applied_modifiers = {}
        evaluated_modifiers = [action.evaluate(variables) for action in self.modifiers]
        for modifier in evaluated_modifiers:
            if modifier.isdigit():
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

    def evaluate(self, variables, arguments=None):
        return ''.join((child.evaluate(variables, arguments=arguments) for child in self.children))

    def perform(self, variables, arguments=None):
        for subaction in self.children:
            subaction.perform(variables, arguments=arguments)

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
        return text

    def var_replace(self, variables, arguments, matchobj):
        match_index = int(matchobj.string[1:])
        if match_index > 0:
            match_index -= 1
        try:
            var = variables[match_index]
        except IndexError:
            return ''
        return var.evaluate(variables, arguments)

    def perform(self, variables, arguments=None):
        api.type_literal(self.evaluate_text(variables, arguments))

    def evaluate(self, variables, arguments=None):
        return self.evaluate_text(variables, arguments)

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

    def perform(self, variables, arguments=None):
        evaluation = self.evaluate(variables, arguments)
        if evaluation is not None:
            api.type_literal(str(evaluation))

    def evaluate(self, variables, arguments=None):
        from sprecgrammars.api import action
        # builtin functions
        if isinstance(self.definition, types.FunctionType):
            args = [a.evaluate(variables, arguments) for a in self.arguments]
            result = self.definition(*args)
            return result
        # user defined functions
        else:
            args = self.get_arguments(variables, arguments)
            return self.definition.action.evaluate(variables, args)

class KeySequence(Action):

    def __init__(self):
        super().__init__()
        self.keys = []

    def add(self, node):
        self.keys.append(node)

    def perform(self, variables, arguments=None):
        keypresses = self.evaluate(variables, arguments)
        api.type_keypresses(keypresses)

    def evaluate(self, variables, arguments=None):
        modifiers = self.apply_modifiers(variables)
        return [node.evaluate(variables, arguments) for node in self.keys] * modifiers.get('repeat', 1)

class PositionalVariable(Action):

    def __init__(self, pos):
        super().__init__()
        self.pos = pos

    def evaluate(self, variables, arguments=None):
        var = variables[self.pos - 1]
        modifiers = self.apply_modifiers(variables)
        result = '' if var is None else var.evaluate(variables, arguments)
        return result * modifiers.get('repeat', 1)

    def perform(self, variables, arguments=None):
        var = variables[self.pos - 1]
        modifiers = self.apply_modifiers(variables)
        if var is not None:
            for i in range(modifiers.get('repeat', 1)):
                var.perform(variables, arguments)

class WhitespaceNode(Action):

    def __init__(self, text):
        super().__init__()
        self.text = text

    def evaluate(self, variables, arguments=None):
        pass

    def perform(self, variables, arguments=None):
        pass

class Argument(Action):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def evaluate(self, variables, arguments=None):
        arguments = {} if arguments is None else arguments
        return arguments.get(self.name, '')

    def perform(self, variables, arguments=None):
        arguments = {} if arguments is None else arguments
        # TODO: add function calls, probably needs extra work
        action = arguments.get(self.name, '')
        api.type_literal(action)