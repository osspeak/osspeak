from sprecgrammars import abstokenstream
from sprecgrammars import tokens

class VocolaTokenStream(abstokenstream.AbstractTokenStream):

    def read_next(self):
        whitespace = self.read_whitespace()
        if self.stream.eof():
            return
        ch = self.stream.peek()
        if ch.isalpha():
            return self.read_word()
        if ch == '|':
            return self.read_ortoken()
        if ch in '()':
            return self.read_paren_token()
        if ch == '_':
            if whitespace:
                self.croak('Repetition must immediately follow a word or grouping')
            return self.read_repetition()
        self.croak('Invalid character: {}'.format(ch))
        

    def read_whitespace(self):
        return self.read_while(lambda ch: ch in ' \n\t')

    def read_word(self):
        val = self.read_while(lambda ch: ch.isalpha())
        return tokens.WordToken(val)

    def read_ortoken(self):
        self.stream.next()
        return tokens.OrToken()

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


    def read_paren_token(self):
        return tokens.ParenToken(self.stream.next())

    def read_digits(self):
        return self.read_while(lambda ch: ch.isdigit())