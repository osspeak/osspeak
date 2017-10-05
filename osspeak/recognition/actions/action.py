from recognition.actions import library
from recognition.actions import context, perform
import platforms.api
import time

class Action:

    def __init__(self, text, defined_functions=None, arguments=None):
        from recognition.actions import pyexpr, asttransform
        self.text = text
        defined_functions = {} if defined_functions is None else defined_functions
        self.namespace = {**defined_functions, **library.namespace}
        try:
            self.literal_expressions, _ = pyexpr.compile_python_expressions(text) if isinstance(text, str) else (text, '')
            self.expressions = [asttransform.transform_expression(e, namespace=self.namespace, arguments=arguments) for e in self.literal_expressions]
        except SyntaxError as e:
            print(f'error: {text}')

    def perform(self, call_locals=None):
        for result in self.generate_results(call_locals):
            perform.perform_io(result)

    def perform_variable(self, call_locals=None, perform_results=False):
        results = []
        for result in self.generate_results(call_locals):
            if perform_results:
                perform.perform_io(result)
            results.append(result)
        return perform.concat_results(results)

    def generate_results(self, call_locals=None):
        recognition_context = perform.get_recognition_context()
        action_globals = {'context': recognition_context, **self.namespace}
        for i, expr in enumerate(self.expressions):
            result = eval(expr, action_globals, call_locals)
            yield result