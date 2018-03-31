from recognition.actions import library, pyexpr, asttransform, context, perform
import keyboard

class Action:
    pass

class SpeechDSLAction(Action):

    def __init__(self, action_input, arguments=None,
                validator=lambda expr: True, raise_on_error=True):
        self.literal_expressions, self.remaining_text = self.compile_expressions(action_input, validator, raise_on_error)
        self.expressions = [asttransform.transform_expression(e, arguments=arguments) for e in self.literal_expressions]

    @property
    def text(self):
        return ''.join(self.literal_expressions)

    def compile_expressions(self, action_input, validator, raise_on_error):
        if isinstance(action_input, str):
            return pyexpr.compile_python_expressions(action_input, validator=validator, raise_on_error=raise_on_error)

    def perform(self, call_locals=None):
        '''
        top level perform
        '''
        typed_previous_result = False
        for result in self.generate_results(call_locals):
            if typed_previous_result and isinstance(result, str):
                result = ' ' + result
            typed_previous_result = perform.perform_io(result)

    def perform_variable(self, call_locals=None, perform_results=False):
        results = []
        for result in self.generate_results(call_locals):
            if perform_results:
                perform.perform_io(result)
            results.append(result)
        return perform.concat_results(results)

    def generate_results(self, call_locals=None):
        recognition_context = perform.get_recognition_context()
        action_globals = {'context': recognition_context, **recognition_context._meta.namespace}
        for i, expr in enumerate(self.expressions):
            result = eval(expr, action_globals, call_locals)
            yield result