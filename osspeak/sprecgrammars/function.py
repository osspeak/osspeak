from inspect import signature, Parameter
import inspect
from sprecgrammars.actions.action import Action


class Function:

    def __init__(self, signature_text, action_text):
        self.signature_text = signature_text
        self.func = self.define_function()
        self.parameters = signature(self.func).parameters
        self.action_text = action_text
        self.name = signature_text.split('(', 1)[0].strip()
        self.action = None

    def get_call_locals(self, args, kwargs):
        call_args = {}
        argpos = 0
        for name, param in self.parameters.items():
            if param.kind == Parameter.POSITIONAL_OR_KEYWORD:
                call_args[name] = args[argpos]
                argpos += 1
        return call_args

    def define_function(self):
        try:
            exec(f'def {self.signature_text}: pass')
        except SyntaxError:
            exec(f'def {self.signature_text}(): pass')
        l = locals()
        for k, v in l.items():
            if k != 'self' or len(l) == 1:
                return v

    def compile_action(self, defined_functions):
        self.action = Action(self.action_text, defined_functions, set(self.parameters.keys()))

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)
        call_locals = self.get_call_locals(args, kwargs)
        return self.action.perform(call_locals)