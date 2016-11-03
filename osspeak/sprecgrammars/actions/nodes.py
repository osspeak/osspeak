from platforms import api

class Action:

    def __init__(self):
        # what follows an underscore, ie {left_2_down}
        self.modifiers = []

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


class RootAction(Action):

    def __init__(self):
        super().__init__()
        self.children = []

    def add(self, child):
        self.children.append(child)

    def evaluate(self, variables, arguments=None):
        return ''.join((child.evaluate(variables, arguments=arguments) for child in self.children))

    def perform(self, variables, arguments=None):
        for subaction in self.children:
            subaction.perform(variables, arguments=arguments)

class LiteralKeysAction(Action):
    
    def __init__(self, text):
        super().__init__()
        self.text = text

    def perform(self, variables, arguments=None):
        api.type_literal(self.text)

    def evaluate(self, variables, arguments=None):
        return self.text

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
        for (param, arg) in zip(self.definition.parameters, self.arguments):
            args[param.name] = arg.evaluate(variables, arguments)
        return args

    def perform(self, variables, arguments=None):
        args = self.get_arguments(variables, arguments)
        self.definition.action.perform(variables, args)

    def evaluate(self, variables, arguments=None):
        args = self.get_arguments(variables, arguments)
        return self.definition.action.evaluate(variables, args)

class KeySequence(Action):

    def __init__(self):
        super().__init__()
        self.keys = []

    def add(self, node):
        self.keys.append(node)

    def perform(self, variables, arguments=None):
        modifiers = self.apply_modifiers(variables)
        keypresses = [node.evaluate(variables, arguments) for node in self.keys] * modifiers.get('repeat', 1)
        api.type_keypresses(keypresses)

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
        print('perform', variables, arguments, self.name)
        arguments = {} if arguments is None else arguments
        # TODO: add function calls, probably needs extra work
        action = arguments.get(self.name, '')
        api.type_literal(action)