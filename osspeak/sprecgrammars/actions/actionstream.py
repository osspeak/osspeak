from sprecgrammars import abstokenstream
from sprecgrammars.actions import tokens

WORD_DELIMITERS = set([
    '{', '}', '(', ')', ',', ' ', '\n', '\t', '+', ',', '|', '=',
    tokens.SliceToken.OPENING_DELIMITER,
    tokens.SliceToken.CLOSING_DELIMITER,
])

class ActionTokenStream(abstokenstream.AbstractTokenStream):

    def __init__(self, text):
        super().__init__(text)
        self.word_delimiters = WORD_DELIMITERS
        self.tokenize_functions = {
            '\t': self.read_whitespace,
            '\n': self.read_whitespace,
            ' ': self.read_whitespace,
            "'": self.read_literal,
            tokens.LiteralTemplateToken.DELIMITER: self.read_template_literal,
            tokens.SliceToken.OPENING_DELIMITER: self.read_slice_token,
            '(': self.read_paren_token,
            ')': self.read_paren_token,
            '{': self.read_brace_token,
            '}': self.read_brace_token,
            '+': self.read_plus_token,
            ',': self.read_comma_token,
            '$': self.read_variable_token,
            '_': self.read_underscore,
        }

    def read_next(self):
        if self.stream.eof():
            return
        ch = self.stream.peek()
        return self.tokenize_functions.get(ch, self.read_word)()

    def read_whitespace(self):
        text = self.read_while(lambda ch: ch in ' \n\t')
        return tokens.WhitespaceToken(text)

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

    def read_template_literal(self):
        text = ''
        self.stream.next()
        while self.stream.peek() != tokens.LiteralTemplateToken.DELIMITER:
            if not self.stream.peek():
                self.croak(f"Missing closing {tokens.LiteralTemplateToken.DELIMITER} character")
            text += self.stream.next()        
        self.stream.next()
        return tokens.LiteralTemplateToken(text)

    def read_word(self):
        text = self._read_word()
        return tokens.WordToken(text)

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

    def read_variable_token(self):
        self.stream.next()
        ch = self.stream.peek()
        if ch.isdigit() or ch == '-':
            return self.read_positional_variable_token()
        return self.read_named_variable_token()

    def read_positional_variable_token(self):
        pos_or_neg_multiplier = 1
        if self.stream.peek() == '-':
            self.stream.next()
            pos_or_neg_multiplier = -1
        position = self.read_while(lambda ch: ch.isdigit())
        if not position:
            self.croak('Positional variable must have a number')
        return tokens.PositionalVariableToken(int(position) * pos_or_neg_multiplier)

    def read_named_variable_token(self):
        if self.stream.eof() or not self.stream.peek().isalpha():
            self.stream.croak()
        name = self.read_while(lambda ch: ch.isalnum())
        return tokens.NamedVariableToken(name)

    def read_underscore(self):
        self.read_while(lambda ch: ch == '_')
        return tokens.UnderscoreToken()
        
    def read_slice_token(self):
        self.stream.next()
        slice_text = self.read_while(lambda ch: ch != tokens.SliceToken.CLOSING_DELIMITER)
        slice_pieces = slice_text.split(':')
        self.stream.next()
        return tokens.SliceToken(slice_pieces)