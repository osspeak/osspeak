import log
from recognition.actions import library

class RecognitionContext:

    def __init__(self, variables, words, namespace, variable_words):
        self.variables = variables
        self.namespace = namespace
        self.arguments = {}
        self.words = words
        self.text = None if words is None else ' '.join(words)

    def get(self, key):
        return self._meta.temp_variables.get(key)

    def set(self, key, value):
        self._meta.temp_variables[key] = value