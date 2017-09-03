class RecognitionResult:

    def __init__(self, variables):
        self.vars = VariableList(variables)

class VariableList:

    def __init__(self, variables):
        self._vars = variables

    def get(self, idx, default=None):
        try:
            return self._vars[idx]
        except IndexError:
            return default