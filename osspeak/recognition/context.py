import log
import platforms.api
from recognition import library

class RecognitionContext:

    def __init__(self, variables):
        self._meta = RecognitionContextMeta(variables)

    def var(self, idx, default=None, perform_results=True):
        from recognition import perform
        try:
            variable_actions = self._meta.variables[idx]
        except IndexError as e:
            raise e
            return default
        return perform.var_result(variable_actions, perform_results) if variable_actions else default

class RecognitionContextMeta:

    def __init__(self, variables):
        self.variables = variables