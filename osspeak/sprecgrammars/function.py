from sprecgrammars.actions.action import Action

class Function:

    def __init__(self, signature_text, action_text):
        self.signature_text = signature_text
        self.validate_signature()
        self.action_text = action_text
        self.name = signature_text.split('(', 1)[0].strip()
        self.action = None

    def validate_signature(self):
        try:
            exec(f'def {self.signature_text}: pass')
        except SyntaxError:
            exec(f'def {self.signature_text}(): pass')

    def compile_action(self, defined_functions):
        self.action = Action(self.action_text, defined_functions)

    def __call__(self, *args, **kwargs):
        print(f'calling function: {self.name}')