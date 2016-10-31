from sprecgrammars.formats.baseparser import BaseParser
from sprecgrammars.actions import actionstream, nodes
from sprecgrammars.actions import tokens
from platforms.actions import mappings

class ActionParser:

    def __init__(self, text):
        self.stream = actionstream.ActionTokenStream(text)
        self.grouped_action_stack = []
        self.grouping_delimiter_flags = {}
        self.append_modifier_flag = False
        self.action_to_modify = None
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
        self.init_grouped_action_stack()
        for tok in self.stream:
            tok_type = type(tok)
            self.parse_map[tok_type](tok)
        return self.grouped_action_stack[0]

    def parse_substitute_action(self):
        self.init_grouped_action_stack()
        for tok in self.stream:
            tok_type = type(tok)
            self.parse_map[tok_type](tok)
            if tok_type is not tokens.WhitespaceToken:
                break
        return self.grouped_action_stack[0]

    def init_grouped_action_stack(self):
        root_action = nodes.RootAction()
        self.grouped_action_stack = [root_action]

    def parse_word_token(self, tok):
        if tok.text not in mappings.action_names:
            return self.parse_literal_token(tok)
        self.parse_function(tok.text)

    def parse_function(self, func_name):
        func = nodes.FunctionCall(func_name)
        self.add_action(func, grouped=True)
        next_token = self.peek()
        if not isinstance(next_token, tokens.ParenToken) or not next_token.is_open:
            self.stream.croak('missing paren')

    def parse_paren(self, tok):
        if tok.is_open:
            return
        self.pop_grouped_action()

    def parse_curly_brace(self, tok):
        if tok.is_open:
            seq = nodes.KeySequence()
            self.add_action(seq, grouped=True)
            return
        self.pop_grouped_action()

    def pop_grouped_action(self):
        if len(self.grouped_action_stack) < 2:
            self.error('too many closing arens')
        self.action_to_modify = self.grouped_action_stack.pop()        

    def parse_plus_sign(self, tok):
        if not isinstance(self.grouped_action_stack[-1], nodes.KeySequence):
            return self.parse_literal_token(tok)
        seq = self.grouped_action_stack[-1]
        self.grouping_delimiter_flags[seq] = False

    def parse_comma_token(self, tok):
        if not isinstance(self.grouped_action_stack[-1], nodes.FunctionCall):
            return self.parse_literal_token(tok)
        seq = self.grouped_action_stack[-1]
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
        self.add_action(var_action)
        
    def parse_literal_token(self, tok):
        literal_action = nodes.LiteralKeysAction(tok.text)
        self.add_action(literal_action)

    def add_action(self, action, grouped=False):
        if self.append_modifier_flag:
            self.action_to_modify.modifiers.append(action)
            self.append_modifier_flag = False
        else:
            self.set_delimiter_flag()
            self.grouped_action_stack[-1].add(action)
        if grouped:
            self.grouped_action_stack.append(action)
            self.grouping_delimiter_flags[action] = False
        self.action_to_modify = action 

    # def add_single_action(self, action):
    #     self.set_delimiter_flag()
    #     self.grouped_action_stack[-1].add(action)

    # def add_grouped_action(self, action):
    #     self.set_delimiter_flag()
    #     self.grouped_action_stack[-1].add(action)
    #     self.grouped_action_stack.append(action)
    #     self.grouping_delimiter_flags[action] = False

    def set_delimiter_flag(self):
        # if top level action is expecting a delimiter (, or +), raise an error
        if len(self.grouped_action_stack) > 1:
            last_action = self.grouped_action_stack[-1]
            if self.grouping_delimiter_flags[last_action]:
                self.error('foobar')
            self.grouping_delimiter_flags[last_action] = True

    def parse_whitespace_token(self, tok):
        return nodes.WhitespaceNode(tok.text)
    
    def parse_underscore_token(self, tok):
        self.append_modifier_flag = True