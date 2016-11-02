from sprecgrammars.functions import stream, tokens, astree
from platforms.actions import mappings

class FunctionDefinitionParser:

    def __init__(self, text):
        self.stream = stream.FunctionDefinitionTokenStream(text)
        self.function = astree.FunctionDefinition()
        self.ready_for_parameter = False
        self.parse_map = {
            tokens.WordToken: self.parse_word_token,
            tokens.ParenToken: self.parse_paren_token,
            tokens.CommaToken: self.parse_comma_token,
            tokens.DefaultActionToken: self.parse_default_action_token,
        }

    def parse(self):
        for tok in self.stream:
            tok_type = type(tok)
            self.parse_map[tok_type](tok)
        return self.function

    def parse_default_action_token(self, tok):
        if self.ready_for_parameter:
            self.error()
        self.function.parameters[-1].default_action = tok.action

    def parse_word_token(self, tok):
        if self.function.name is None:
            self.function.name = tok.text
        elif self.ready_for_parameter:
            self.function.parameters.append(astree.FunctionParameter(tok.text))
            self.ready_for_parameter = False
        else:
            self.error('Unexpected literal')

    def parse_paren_token(self, tok):
        if self.function.name is None:
            self.croak()
        if tok.is_open:
            if self.ready_for_parameter or self.function.parameters:
                self.error()
            self.ready_for_parameter = True
        else:
            if (not self.ready_for_parameter and not self.function.parameters) or (self.ready_for_parameter and self.function.parameters) or not self.eof():
                self.error()

    def parse_comma_token(self, tok):
        if self.ready_for_parameter:
            self.error()
        self.ready_for_parameter = True

    def error(self, msg='generic error'):
        self.stream.croak(msg)

    def eof(self):
        return self.stream.peek() is None
