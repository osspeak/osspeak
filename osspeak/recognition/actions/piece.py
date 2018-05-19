from recognition.actions import library, pyexpr, asttransform, context, perform

class ActionPiece:

    def __init__(self):
        self.json_object = None

    def perform(self):
        raise NotImplementedError

    @classmethod
    def from_object(cls, obj, *a, **kw):
        factory_map = {
            'dsl': DSLActionPiece
        }
        constructor = factory_map[obj['type']]
        instance = constructor(obj['value'], *a, **kw)
        instance.json_object = obj
        return instance

class DSLActionPiece(ActionPiece):
    
    def __init__(self, action_input, arguments=None,
                validator=lambda expr: True, raise_on_error=True):
        super().__init__()
        self.literal_expressions, self.remaining_text = self.compile_expressions(action_input, validator, raise_on_error)
        self.expressions = [asttransform.transform_expression(e, arguments=arguments) for e in self.literal_expressions]

    def compile_expressions(self, action_input, validator, raise_on_error):
        if isinstance(action_input, str):
            return pyexpr.compile_python_expressions(action_input, validator=validator, raise_on_error=raise_on_error)

    def perform(self, call_locals=None):
        '''
        top level perform
        '''
        typed_previous_result = False
        _globals = perform.recognition_namespace()
        for result in self.generate_results(_globals, call_locals):
            if typed_previous_result and isinstance(result, str):
                result = ' ' + result
            typed_previous_result = perform.perform_io(result)

    def perform_variable(self, call_locals=None, perform_results=False):
        results = []
        _globals = perform.recognition_namespace()
        for result in self.generate_results(_globals, call_locals):
            if perform_results:
                perform.perform_io(result)
            results.append(result)
        return perform.concat_results(results)

    def generate_results(self, _globals, call_locals):
        for i, expr in enumerate(self.expressions):
            result = eval(expr, _globals, call_locals)
            yield result

class Snippet:

    def __init__(self, text):
        super().__init__()
        self.text = text