from sprecgrammars.formats.baseparser import BaseParser
from sprecgrammars.actions import actionstream, nodes
from sprecgrammars.actions import tokens
from platforms.actions import mappings

class ActionParser:

    def __init__(self, text):
        self.stream = actionstream.ActionTokenStream(text)
        self.action_stack = []
        self.grouping_delimiter_flags = {}
        self.parse_map = {
            tokens.LiteralToken: self.parse_literal_token,
            tokens.WordToken: self.parse_word_token,
            tokens.ParenToken: self.parse_paren,
            tokens.BraceToken: self.parse_curly_brace,
            tokens.PlusToken: self.parse_plus_sign,
            tokens.CommaToken: self.parse_plus_sign,
            tokens.PositionalVariableToken: self.parse_positional_variable_token,
            tokens.WhitespaceToken: self.parse_whitespace_token,
            tokens.UnderscoreToken: self.parse_underscore_token,
        }

    def parse(self):
        self.init_action_stack()
        for tok in self.stream:
           self.parse_map[type(tok)](tok)
        return self.action_stack[0]

    def parse_substitute_action(self):
        self.init_action_stack()
        for tok in self.stream:
           self.parse_map[type(tok)](tok)
           break
        return self.action_stack[0]

    def init_action_stack(self):
        root_action = nodes.RootAction()
        self.action_stack = [root_action]

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

    def parse_positional_variable_token(self, tok):
        var_action = nodes.PositionalVariable(tok.pos)
        self.add_single_action(var_action)
        
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

    def parse_whitespace_token(self, tok):
        pass
    
    def parse_underscore_token(self, tok):
        pass