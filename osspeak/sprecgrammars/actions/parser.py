from osspeak.sprecgrammars.formats.baseparser import BaseParser
from osspeak.sprecgrammars.actions import actionstream, nodes
from osspeak.sprecgrammars.actions import tokens


class ActionParser(BaseParser):

    def __init__(self, text):
        super().__init__(text)
        self.stream = actionstream.ActionTokenStream(self.text)
        self.action_stack = []
        self.parse_map = {
            tokens.LiteralToken: self.parse_literal_token,
            # tokens.OrToken: self.parse_or_token,
            # tokens.ParenToken: self.parse_paren_token,
        }

    def parse(self):
        action = nodes.Action()
        self.action_stack = [action]
        for tok in self.stream:
            self.parse_map[type(tok)](tok)
        return action

    def parse_literal_token(self, tok):
        literal_action = nodes.LiteralKeysAction(tok.text)
        self.action_stack[-1].children.append(literal_action)

    def parse_or_token(self, tok):
        or_node = astree.OrNode()
        self.action_stack[-1].children.append(or_node)

    def parse_paren_token(self, tok):
        pass
