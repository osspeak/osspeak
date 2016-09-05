from sprecgrammars import abstokenstream
from sprecgrammars.actions import tokens

WORD_DELIMETERS = set(['{', '}', '(', ')', ', ', ' ', '\n', '\t', '+', ','])

class ActionTokenStream(abstokenstream.AbstractTokenStream):

    def read_next(self):
        self.read_while(lambda ch: ch in ' \n\t')
        if self.stream.eof():
            return
        ch = self.stream.peek()
        if ch == "'":
            return self.read_literal()
        if ch in '()':
            return self.read_paren_token()
        if ch in '{}':
            return self.read_brace_token()
        if ch == '+':
            return self.read_plus_token()
        if ch == ',':
            return self.read_comma_token()
        return self.read_word()

    def read_literal(self):
        literal_text = ''
        # skip first apostrophe
        self.stream.next()
        while self.stream.peek() != "'":
            if not self.stream.peek():
                self.croak("Missing closing ' character")
            literal_text += self.stream.next()
        # skip last apostrophe
        self.stream.next()
        return tokens.LiteralToken(literal_text)

    def read_word(self):
        literal_text = ''
        while not self.stream.eof() and self.stream.peek() not in WORD_DELIMETERS:
            literal_text += self.stream.next()
        return tokens.WordToken(literal_text)

    def read_paren_token(self):
        return tokens.ParenToken(self.stream.next())

    def read_brace_token(self):
        return tokens.BraceToken(self.stream.next())

    def read_plus_token(self):
        self.stream.next()
        return tokens.PlusToken()

    def read_comma_token(self):
        self.stream.next()
        return tokens.CommaToken()