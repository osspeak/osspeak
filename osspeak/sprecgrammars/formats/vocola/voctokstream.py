from osspeak.sprecgrammars import abstokenstream
from osspeak.sprecgrammars import tokens

class VocolaTokenStream(abstokenstream.AbstractTokenStream):

    def read_next(self):
        self.read_while(lambda ch: ch in ' \n\t')
        if self.stream.eof():
            return
        ch = self.stream.peek()
        if ch.isalpha():
            return self.read_word()
        if ch == '|':
            return self.read_ortoken()
        if ch in '()':
            print('asdasd')
            return self.read_paren_token()
        self.croak('Invalid character: {}'.format(ch))
        

    def read_word(self):
        val = self.read_while(lambda ch: ch.isalpha())
        return tokens.WordToken(val)

    def read_ortoken(self):
        self.stream.next()
        return tokens.OrToken()

    def read_paren_token(self):
        return tokens.ParenToken(self.stream.next())

        # public override Token ReadNext()
        # {
        #     ReadWhile(IsWhitespace);
        #     if (Input.Eof() == true) return null;
        #     string ch = Input.Peek();
        #     if (WordRegex.IsMatch(ch)) return ReadWord();
        #     if (ch == "(" || ch == ")") return ReadParen();
        #     if (ch == "|") return ReadOr();
        #     Croak("Invalid Character: " + ch);
        #     return null;
        # }