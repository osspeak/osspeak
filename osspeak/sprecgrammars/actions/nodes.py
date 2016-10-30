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

    def evaluate(self, variables):
        return ''.join((child.evaluate(variables) for child in self.children))

    def perform(self, variables):
        for subaction in self.children:
            subaction.perform(variables)

class LiteralKeysAction(Action):
    
    def __init__(self, text):
        super().__init__()
        self.text = text

    def perform(self, variables):
        api.type_literal(self.text)

    def evaluate(self, variables):
        return self.text

class FunctionCall(Action):

    def __init__(self, func_name):
        super().__init__()
        self.arguments = []
        self.func_name = func_name

    def add(self, node):
        self.arguments.append(node)

class KeySequence(Action):

    def __init__(self):
        super().__init__()
        self.keys = []

    def add(self, node):
        self.keys.append(node)

    def perform(self, variables):
        modifiers = self.apply_modifiers(variables)
        keypresses = [node.evaluate(variables) for node in self.keys] * modifiers.get('repeat', 1)
        api.type_keypresses(keypresses)

class PositionalVariable(Action):

    def __init__(self, pos):
        super().__init__()
        self.pos = pos

    def evaluate(self, variables):
        var = variables[self.pos - 1]
        return '' if var is None else var.evaluate(variables)

    def perform(self, variables):
        var = variables[self.pos - 1]
        if var is not None:
            var.perform(variables)

class WhitespaceNode(Action):

    def __init__(self, text):
        super().__init__()
        self.text = text

    def evaluate(self, variables):
        pass

    def perform(self, variables):
        pass