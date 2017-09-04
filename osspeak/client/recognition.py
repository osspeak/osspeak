class RecognitionResult:

    def __init__(self, variables):
        self.vars = VariableList(variables)

class VariableList:

    def __init__(self, variables):
        self._vars = variables

    def perform(self, idx, default=None):
        try:
            variable_actions = self._vars[idx]
        except IndexError:
            return default
        results = []
        for action in variable_actions:
            results.append(action.perform())
        return results[0]