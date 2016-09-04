from sprecgrammars.formats.baseparser import BaseParser
from sprecgrammars.actions import actionstream, nodes
from sprecgrammars.actions import tokens
from platforms.actions import mappings

class ActionParser(BaseParser):

    def __init__(self, text):
        super().__init__(text)
        self.stream = actionstream.ActionTokenStream(self.text)
        self.action_stack = []
        self.read_pos = 0
        self.parse_pos = 0
        self.arg_tokens_stack = []
        self.parse_map = {
            tokens.LiteralToken: self.parse_literal_token,
            tokens.WordToken: self.parse_word_token,
        }

    def parse(self):
        action = nodes.RootAction()
        self.action_stack = [action]
        for tok in self.stream:
            self.parse_map[type(tok)](tok)
        return action

    def parse_token(self, tok):


    def parse_word_token(self, tok):
        if tok.text not in mappings.action_names:
            return self.parse_literal_token(tok)
        self.parse_function(tok.text)

    def parse_function(self, func_name):
        next_token = self.peek()
        print('next', self.top_level_token_iterator)
        if not isinstance(next_token, tokens.ParenToken) or not next_token.is_open:
            self.stream.croak('missing paren')
        self.action_stack.append(nodes.FunctionCall(func_name))
        # discard opening paren token
        self.arg_tokens_stack.append({'pos': 0, 'tokens': self.get_arg_tokens()})
        self.parse_function_args()
        self.action_stack.pop()
        self.arg_tokens_stack.pop()

    def parse_function_args(self):
        token_iterator = self.top_level_token_iterator
        print('weasel', token_iterator)
        for tok in token_iterator:
            parse_func = self.parse_map[type(tok)](tok)

    def get_arg_tokens(self):
        open_count = 0
        arg_tokens = []
        token_iterator = self.top_level_token_iterator
        for tok in token_iterator:
            arg_tokens.append(tok)
            if isinstance(tok, tokens.ParenToken):
                if tok.is_open:
                    open_count += 1
                else:
                    open_count -= 1
                    if open_count < 0:
                        self.stream.croak('too many close parens')
                    if open_count == 0:
                        return arg_tokens
        self.stream.croak('too many open parens')

    @property
    def top_level_token_iterator(self):
        if not self.arg_tokens_stack:
            return self.stream
        arg_tokens = self.arg_tokens_stack[-1]
        tokens = []
        while arg_tokens['pos'] < len(arg_tokens['tokens']):
            tokens.append(arg_tokens['tokens'][arg_tokens['pos']])
            arg_tokens['pos'] += 1
        return tokens

    def next(self):
        if not self.arg_tokens_stack:
            return self.stream.next()
        last = self.arg_tokens_stack[-1]
        next_tok = last['tokens'][last['pos']]
        last['pos'] += 1
        return next_tok

    def peek(self):
        if not self.arg_tokens_stack:
            return self.stream.peek()
        if self.arg_tokens_stack[-1]['pos'] + 1 > len(self.arg_tokens_stack[-1]['tokens']):
            return
        return self.arg_tokens_stack[-1]['tokens'][self.arg_tokens_stack[-1]['pos']]

    def eof():
        return self.peek() is None
        
    def parse_literal_token(self, tok):
        literal_action = nodes.LiteralKeysAction(tok.text)
        self.action_stack[-1].add(literal_action)

    def parse_arguments(self, func_node, arg_tokens):
        or_node = astree.OrNode()
        self.action_stack[-1].add(or_node)

