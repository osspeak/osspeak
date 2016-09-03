from sprecgrammars.formats.baseparser import BaseParser
from sprecgrammars.actions import actionstream, nodes
from sprecgrammars.actions import tokens
from platforms.actions import mappings

class ActionParser(BaseParser):

    def __init__(self, text):
        super().__init__(text)
        self.stream = actionstream.ActionTokenStream(self.text)
        self.action_stack = []
        self.func_stack = []
        self.parse_map = {
            tokens.LiteralToken: self.parse_literal_token,
            tokens.WordToken: self.parse_word_token,
            # tokens.OrToken: self.parse_or_token,
            # tokens.ParenToken: self.parse_paren_token,
        }

    def parse(self):
        action = nodes.Action()
        self.action_stack = [action]
        for tok in self.stream:
            self.parse_map[type(tok)](tok)
        return action

    def parse_word_token(self, tok):
        if tok.text not in mappings.action_names:
            return self.parse_literal_token(tok)
        next_token = self.stream.peek()
        if not isinstance(next_token, tokens.ParenToken) or not next_token.is_open:
            self.stream.croak('missing paren')
        
        print('foo')

    def parse_literal_token(self, tok):
        literal_action = nodes.LiteralKeysAction(tok.text)
        self.action_stack[-1].children.append(literal_action)

    def parse_arguments(self, func_node, arg_tokens):
        or_node = astree.OrNode()
        self.action_stack[-1].children.append(or_node)

    def parse_paren_token(self, tok):
        pass
