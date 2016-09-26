from sprecgrammars.formats.baseparser import BaseParser
from sprecgrammars.actions import actionstream, nodes
from sprecgrammars.actions import tokens
from platforms.actions import mappings

class ActionParser(BaseParser):

    def __init__(self, text):
        super().__init__(text)
        self.stream = actionstream.ActionTokenStream(self.text)
        self.action_stack = []
        self.grouping_delimiter_flags = {}
        self.parse_map = {
            tokens.LiteralToken: self.parse_literal_token,
            tokens.WordToken: self.parse_word_token,
            tokens.ParenToken: self.parse_paren,
            tokens.BraceToken: self.parse_curly_brace,
            tokens.PlusToken: self.parse_plus_sign,
            tokens.CommaToken: self.parse_plus_sign,
        }

    def parse(self):
        root_action = nodes.RootAction()
        self.action_stack = [root_action]
        for tok in self.stream:
           self.parse_map[type(tok)](tok)
        return root_action

    def parse_word_token(self, tok):
        if tok.text not in mappings.action_names:
            return self.parse_literal_token(tok)
        self.parse_function(tok.text)

    def parse_function(self, func_name):
        func = nodes.FunctionCall(func_name)
        self.add_grouped_action(func)
        next_token = self.peek()
        if not isinstance(next_token, tokens.ParenToken) or not next_token.is_open:
            self.stream.croak('missing paren')

    def parse_paren(self, tok):
        if tok.is_open:
            return
        if len(self.action_stack) < 2:
            self.error('too many closing arens')
        self.action_stack.pop()

    def parse_curly_brace(self, tok):
        if tok.is_open:
            seq = nodes.KeySequence()
            self.add_grouped_action(seq)
            return
        if len(self.action_stack) < 2:
            self.error('too many closing arens')
        self.action_stack.pop()

    def parse_plus_sign(self, tok):
        if not isinstance(self.action_stack[-1], nodes.KeySequence):
            return self.parse_literal_token(tok)
        seq = self.action_stack[-1]
        self.grouping_delimiter_flags[seq] = False

    def parse_comma_token(self, tok):
        if not isinstance(self.action_stack[-1], nodes.FunctionCall):
            return self.parse_literal_token(tok)
        seq = self.action_stack[-1]
        self.grouping_delimiter_flags[seq] = False        

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
        self.add_single_action(literal_action)

    def add_single_action(self, action):
        self.set_delimiter_flag()
        self.action_stack[-1].add(action)

    def add_grouped_action(self, action):
        self.set_delimiter_flag()
        self.action_stack[-1].add(action)
        self.action_stack.append(action)
        self.grouping_delimiter_flags[action] = False

    def set_delimiter_flag(self):
        # if top level action is expecting a delimiter (, or +), raise an error
        if len(self.action_stack) > 1:
            if self.grouping_delimiter_flags[self.action_stack[-1]]:
                self.error('foobar')
            self.grouping_delimiter_flags[self.action_stack[-1]] = True

