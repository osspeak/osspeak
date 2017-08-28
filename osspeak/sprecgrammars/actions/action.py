from sprecgrammars.actions import pyexpr, asttransform

class Action:

    def __init__(self, text, defined_functions):
        # namespace = set({} if defined_functions is None else defined_functions)
        namespace = set()
        try:
            expressions = pyexpr.compile_python_expressions(text)
            self.expressions = [asttransform.transform_expression(e, namespace=namespace) for e in expressions]
        except SyntaxError as e:
            print(f'error: {text}')