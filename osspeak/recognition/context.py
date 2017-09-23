import log
import platforms.api
from recognition import library

class RecognitionContext:

    def __init__(self, variables):
        self.vars = VariableList(variables)

    def var(self, idx, default=None, perform_results=True):
        from recognition import perform
        try:
            variable_actions = self._vars[idx]
        except IndexError as e:
            raise e
            return default
        return perform.var_result(variable_actions, perform_results) if variable_actions else default

class VariableList:

    def __init__(self, variables):
        self._vars = variables

    def get(self, idx, default=None, perform_results=True):
        from recognition import perform
        try:
            variable_actions = self._vars[idx]
        except IndexError as e:
            raise e
            return default
        return perform.var_result(variable_actions, perform_results) if variable_actions else default