from recognition import inputstream
from recognition.rules import tokens

token_character_map = {
    '|': tokens.OrToken,
    '(': tokens.GroupingOpeningToken,
    ')': tokens.GroupingClosingToken,
    '[': tokens.OptionalGroupingOpeningToken,
    ']': tokens.OptionalGroupingClosingToken,
}

class RuleTokenStream:

    def __init__(self, text, defined_functions=None):
        self.stream = inputstream.InputStream(text)
        self.peeked_token = None
        self.defined_functions = {} if defined_functions is None else defined_functions

    def read_next(self):
        whitespace = self.read_whitespace()
        if self.stream.eof():
            return
        ch = self.stream.peek()
        if ch.isalnum():
            return self.read_word()
        if ch in token_character_map:
            self.stream.next()
            return token_character_map[ch]()
        if ch == '<':
            return self.read_named_rule()
        if ch == '=':
            return self.read_action_substitute()
        if ch == '_':
            if whitespace:
                self.croak('Repetition must immediately follow a word or grouping')
            return self.read_repetition()
        self.croak(f'Invalid character: {ch}')

    def read_whitespace(self):
        return self.read_while(lambda ch: ch in ' \n\t')

    def read_word(self):
        val = self.read_while(lambda ch: ch.isalnum())
        return tokens.WordToken(val)

    def read_repetition(self):
        '''
        Ex: left_3 or (hello|goodbye)_3-9 for inclusive ranges
        Dash indicates range, low/high both optional, low defaults to
        0, high defaults to infinity
        '''
        # skip first underscore
        assert self.stream.next() == '_'
        low = self.read_digits() or 0
        high = low
        if self.stream.peek() == '-':
            self.stream.next()
            high = self.read_digits() or None
        return tokens.RepetitionToken(low=low, high=high)

    def read_digits(self):
        return self.read_while(lambda ch: ch.isdigit())

    def read_named_rule(self):
        var_name = self.read_while(lambda ch: ch != '>')
        self.stream.next()
        return tokens.NamedRuleToken(var_name[1:])

    def read_action_substitute(self):
        assert self.stream.next() == '='
        remaining_text = self.stream.text[self.stream.pos:]
        tok = tokens.ActionSubstituteToken(remaining_text, self.defined_functions)
        # could increase self.stream.stream.pos, but better to use
        # stream interface
        for i in range(tok.consumed_char_count):
            self.stream.next()
        return tok

    def next(self):
        tok = self.peeked_token
        self.peeked_token = None
        return self.read_next() if tok is None else tok

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
