from sprecgrammars import inputstream
import re

WORD_DELIMITERS = set(['{', '}', '(', ')', ',', ' ', '\n', '\t', '+', ','])

class AbstractTokenStream:

    word_regex = re.compile(r'[a-zA-Z]')

    def __init__(self, text):
        self.stream = inputstream.InputStream(text)
        self.current = None

    def next(self):
        tok = self.current
        self.current = None
        return self.read_next() if tok is None else tok

    def _read_word(self):
        literal_text = ''
        while not self.stream.eof() and self.stream.peek() not in WORD_DELIMITERS:
            literal_text += self.stream.next()
        return literal_text

    def peek(self):
        if self.current is not None:
            return self.current
        self.current = self.read_next()
        return self.current

    def eof(self):
        return self.peek() is None

    def croak(self, text):
        raise RuntimeError(text)

    def read_while(self, predicate):
        val = ''
        while not self.stream.eof() and predicate(self.stream.peek()):
            val += self.stream.next()
        return val

    def __iter__(self):
        while not self.eof():
            yield self.next()
