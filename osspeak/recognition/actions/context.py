import log
from recognition.actions import library

class RecognitionContext:

    def __init__(self, variables, words, namespace):
        self._meta = RecognitionContextMeta(variables, namespace)
        self.words = words
        self.text = None if words is None else ' '.join(words)

    def get(self, key):
        return self._meta.temp_variables.get(key)

    def set(self, key, value):
        self._meta.temp_variables[key] = value

    def __getitem__(self, i):
        return self._meta.var(i, perform_results=False)

class RecognitionContextMeta:

    def __init__(self, variables, namespace):
        self.variables = variables
        self.temp_variables = {}
        self.namespace = namespace

    def call_or_type(self, value):
        return CallOrType(value)

    def var(self, idx, default=None, perform_results=True):
        from recognition.actions import perform
        try:
            variable_action_pieces = self.variables[idx]
        except IndexError as e:
            return default
        return perform.var_result(variable_action_pieces, perform_results) if variable_action_pieces else default

class CallOrType(str):

    FUNC_MAP = {
        'if': library.flow.osspeak_if,
        'while': library.flow.osspeak_while
    }

    def __init__(self, func_name):
        self.func_name = func_name
        self.func = self.FUNC_MAP[func_name]

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return self.func_name