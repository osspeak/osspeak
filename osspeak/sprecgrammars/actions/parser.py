from sprecgrammars.formats.baseparser import BaseParser
from sprecgrammars.actions import actionstream, nodes
from sprecgrammars.actions import tokens
from platforms.actions import mappings

class ActionParser(BaseParser):

    def __init__(self, text):
        super().__init__(text)
        self.stream = actionstream.ActionTokenStream(self.text)
        self.action_stack = []
        self.parse_map = {
            tokens.LiteralToken: self.parse_literal_token,
            tokens.WordToken: self.parse_word_token,
            tokens.ParenToken: self.parse_paren,
        }

    def parse(self):
        action = nodes.RootAction()
        self.action_stack = [action]
        for tok in self.stream:
            print(tok)
            self.parse_map[type(tok)](tok)
        print(action.children[-1].arguments)
        return action

    def parse_word_token(self, tok):
        if tok.text not in mappings.action_names:
            return self.parse_literal_token(tok)
        self.parse_function(tok.text)

    def parse_function(self, func_name):
        func = nodes.FunctionCall(func_name)
        self.action_stack[-1].add(func)
        self.action_stack.append(func)
        next_token = self.peek()
        if not isinstance(next_token, tokens.ParenToken) or not next_token.is_open:
            self.stream.croak('missing paren')

    def parse_paren(self, tok):
        if tok.is_open:
            return
        if len(self.action_stack) < 2:
            self.error('too many closing arens')
        self.action_stack.pop()

    def next(self):
        return self.stream.next()

    def peek(self):
        return self.stream.peek()

    def error(self, msg):
        self.stream.croak(msg)

    def eof():
        return self.peek() is None
        
    def parse_literal_token(self, tok):
        literal_action = nodes.LiteralKeysAction(tok.text)
        self.action_stack[-1].add(literal_action)

