class Action:

    def __init__(self, text, defined_functions=None):
        from sprecgrammars.actions import pyexpr, asttransform
        from sprecgrammars.functions import library

        builtins = __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)
        defined_functions = {} if defined_functions is None else defined_functions
        self.text = text
        self.namespace = {**defined_functions, **library.builtin_functions, **builtins}
        try:
            expressions = pyexpr.compile_python_expressions(text) if isinstance(text, str) else text
            self.expressions = [asttransform.transform_expression(e, namespace=self.namespace) for e in expressions]
        except SyntaxError as e:
            print(f'error: {text}')

    def perform(self, recognition_result=None):
        if recognition_result is None:
            action_globals = {'result': recognition_result, **self.namespace}
        else:
            action_globals = globals()
            print('ag', list(action_globals.keys()), list(locals().keys()))
        results = []
        for expr in self.expressions:
            result = eval(expr, action_globals)
            results.append(result)
        return results