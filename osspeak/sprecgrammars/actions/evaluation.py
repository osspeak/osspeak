class RootActionEvaluation:

    def __init__(self, literals):
        self.literals = literals

    def __mul__(self, other):
        return self

    def __rmul__(self, other):
        return self