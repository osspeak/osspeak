from client import recognition

class Action:

    def __init__(self, text, defined_functions=None):
        from sprecgrammars.actions import pyexpr, asttransform
        self.text = text
        defined_functions = {} if defined_functions is None else defined_functions
        self.namespace = {**defined_functions, **recognition.namespace}
        try:
            expressions = pyexpr.compile_python_expressions(text) if isinstance(text, str) else text
            self.expressions = [asttransform.transform_expression(e, namespace=self.namespace) for e in expressions]
        except SyntaxError as e:
            print(f'error: {text}')

    def perform(self, recognition_result=None):
        if recognition_result is None:
            action_globals = globals()
        else:
            action_globals = {'result': recognition_result, **self.namespace}
        results = []
        for expr in self.expressions:
            result = eval(expr, action_globals)
            results.append(result)
        return results