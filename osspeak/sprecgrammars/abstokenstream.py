from sprecgrammars import inputstream
import re

WORD_DELIMITERS = set(['{', '}', '(', ')', ',', ' ', '\n', '\t', '+', ',', '|', '='])

class AbstractTokenStream:

    word_regex = re.compile(r'[a-zA-Z]')

    def __init__(self, text):
        self.stream = inputstream.InputStream(text)
        self.word_delimiters = WORD_DELIMITERS
        self.peeked_token = None

    def next(self):
        tok = self.peeked_token
        self.peeked_token = None
        return self.read_next() if tok is None else tok

    def _read_word(self):
        literal_text = ''
        while not self.stream.eof() and self.stream.peek() not in self.word_delimiters:
            literal_text += self.stream.next()
        return literal_text

    def peek(self):
        if self.peeked_token is not None:
            return self.peeked_token
        self.peeked_token = self.read_next()
        return self.peeked_token

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
