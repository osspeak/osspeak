from client import recognition
import platforms.api
import time

class Action:

    def __init__(self, text, defined_functions=None, arguments=None):
        from sprecgrammars.actions import pyexpr, asttransform
        self.text = text
        defined_functions = {} if defined_functions is None else defined_functions
        self.namespace = {**defined_functions, **recognition.namespace}
        try:
            self.literal_expressions = pyexpr.compile_python_expressions(text) if isinstance(text, str) else text
            self.expressions = [asttransform.transform_expression(e, namespace=self.namespace, arguments=arguments) for e in self.literal_expressions]
        except SyntaxError as e:
            print(f'error: {text}')

    def perform(self, call_locals=None):
        for result in self.generate_results(call_locals):
            recognition.perform_io(result)

    def generate_results(self, call_locals=None):
        recognition_result = recognition.get_recognition_result()
        action_globals = {'result': recognition_result, **self.namespace}
        for expr in self.expressions:
            result = eval(expr, action_globals, call_locals)
            yield result