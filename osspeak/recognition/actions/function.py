import inspect
from inspect import signature, Parameter
from recognition.actions import piece

class Function:

    def __init__(self, signature_text, action_input):
        self.signature_text = signature_text
        self.func = self.define_function()
        self.parameters = signature(self.func).parameters
        self.name = signature_text.split('(', 1)[0].strip()
        self.action_input = action_input
        self.action_pieces = None
        # self.action_pieces = action_input

    def get_call_locals(self, args, kwargs):
        call_args = kwargs.copy()
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

    def compile_action_pieces(self):
        from recognition.actions import piece
        arguments = set(self.parameters.keys())
        action_input = self.action_input
        if not isinstance (action_input, list):
            action_input = [action_input]
        action_objects = [{'type': 'dsl', 'value': x} if isinstance(x, str) else x for x in action_input]
        self.action_pieces = [piece.ActionPiece.from_object(obj, arguments=arguments) for obj in action_objects]

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)
        call_locals = self.get_call_locals(args, kwargs)
        results = []
        for piece in self.action_pieces:
            results.append(piece.perform(call_locals))
        return results[0] if len(results) == 1 else results