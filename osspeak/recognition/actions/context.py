import log
from recognition.actions import library

class RecognitionContext:

    def __init__(self, variables, words, namespace, variable_words):
        self.variables = variables
        self.namespace = namespace
        self.argument_frames = []
        self.words = words
        self.text = None if words is None else ' '.join(words)

def empty_recognition_context():
    return RecognitionContext([], [], {}, [])