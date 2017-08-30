from sprecgrammars.actions import pyexpr, asttransform
from sprecgrammars.functions import library

class Action:

    def __init__(self, text, defined_functions):
        builtins = __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)
        namespace = {} if defined_functions is None else defined_functions
        namespace = {**namespace, **library.builtin_functions, **builtins}
        try:
            expressions = pyexpr.compile_python_expressions(text)
            self.expressions = [asttransform.transform_expression(e, namespace=namespace) for e in expressions]
        except SyntaxError as e:
            print(f'error: {text}')

    def perform(self):
        results = []
        for expr in self.expressions:
            result = eval(expr)