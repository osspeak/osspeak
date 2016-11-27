from sprecgrammars import abstokenstream
from sprecgrammars.functions import tokens

class FunctionDefinitionTokenStream(abstokenstream.AbstractTokenStream):

    def read_next(self):
        self.read_whitespace()
        if self.stream.eof():
            return
        ch = self.stream.peek()
        if ch.isalpha():
            return self.read_word()
        if ch in '()':
            return self.read_paren_token()
        if ch == ',':
            return self.read_comma_token()
        if ch == '=':
            return self.read_default_action()
        self.croak('Invalid character: {}'.format(ch))

    def read_whitespace(self):
        return self.read_while(lambda ch: ch in ' \n\t')

    def read_word(self):
        word_text = self._read_word()
        return tokens.WordToken(word_text)

    def read_paren_token(self):
        return tokens.ParenToken(self.stream.next())

    def read_comma_token(self):
        self.stream.next()
        return tokens.CommaToken()

    def read_default_action(self):
        assert self.stream.next() == '='
        remaining_text = self.stream.text[self.stream.pos:]
        tok = tokens.DefaultActionToken(remaining_text)
        # could increase self.stream.stream.pos, but better to use
        # stream interface
        for i in range(tok.consumed_char_count):
            self.stream.next()
        return tok