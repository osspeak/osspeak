from osspeak.sprecgrammars import abstokenstream
from osspeak.sprecgrammars.actions import tokens

class ActionTokenStream(abstokenstream.AbstractTokenStream):

    def read_next(self):
        self.read_while(lambda ch: ch in ' \n\t')
        if self.stream.eof():
            return
        ch = self.stream.peek()
        if ch == "'":
            return self.read_literal()
        return self.read_word_literal()

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

    def read_word_literal(self):
        literal_text = ''
        while self.stream.peek() not in (None, '\n', '\t'):
            literal_text += self.stream.next()
        return tokens.LiteralToken(literal_text)

    def read_word(self):
        val = self.read_while(lambda ch: ch.isalpha())
        return tokens.WordToken(val)

    def read_ortoken(self):
        self.stream.next()
        return tokens.OrToken()