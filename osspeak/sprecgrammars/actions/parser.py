from sprecgrammars.actions import actionstream, nodes, tokens
from sprecgrammars.functions import library
from platforms.actions import mappings

class ActionParser:

    def __init__(self, text, defined_functions=None):
        self.stream = actionstream.ActionTokenStream(text)
        self.defined_functions = {} if defined_functions is None else defined_functions
        self.grouped_action_stack = []
        self.grouping_delimiter_flags = {}
        self.append_modifier_flag = False
        self.action_to_modify = None
        self.parsed_tokens = []
        self.parse_map = {
            tokens.LiteralToken: self.parse_literal_token,
            tokens.LiteralTemplateToken: self.parse_literal_template_token,
            tokens.WordToken: self.parse_word_token,
            tokens.GroupingOpeningToken: self.parse_open_grouping_token, # (
            tokens.GroupingClosingToken: self.parse_closing_grouping_token, # )
            tokens.KeySequenceOpeningToken: lambda t: self.add_action(nodes.KeySequence(), grouped=True), # {
            tokens.KeySequenceClosingToken: lambda t: self.pop_grouped_action(t), # }
            tokens.PlusToken: self.parse_plus_sign,
            tokens.CommaToken: self.parse_comma_token,
            tokens.NumberToken: self.parse_number_token,
            tokens.PositionalVariableToken: self.parse_positional_variable_token,
            tokens.NamedVariableToken: self.parse_named_variable_token,
            tokens.WhitespaceToken: self.parse_whitespace_token,
            tokens.UnderscoreToken: self.parse_underscore_token,
            tokens.SliceToken: self.parse_slice_token,
        }

    def parse(self, substitute=False):
        tok_types = set()
        self.add_grouped_action()
        for tok in self.stream:
            tok_type = type(tok)
            self.parse_map[tok_type](tok)
            self.parsed_tokens.append(tok)
            tok_types.add(tok_type)
            if substitute:
                if isinstance(tok, tokens.WhitespaceToken) and len(tok_types) == 1:
                    # ignore initial whitespace
                    continue
                if len(self.grouped_action_stack) == 1:
                    break
        if len(self.grouped_action_stack) > 1:
            self.croak('Insufficient closing grouping characters')
        return self.grouped_action_stack[0]

    def add_grouped_action(self):
        root_action = nodes.RootAction()
        self.grouped_action_stack.append(root_action)

    def parse_word_token(self, tok):
        next_token = self.peek()
        if isinstance(next_token, tokens.GroupingOpeningToken):
            # assume it's a function if next char is '(' with no whitespace first
            if tok.text in library.builtin_functions:
                self.parse_function(tok.text, library.builtin_functions[tok.text]) 
            elif tok.text in self.defined_functions:
                self.parse_function(tok.text, self.defined_functions[tok.text])
            else:
                self.stream.croak(f'Invalid function name {tok.text}')
        else:
            return self.parse_literal_token(tok)

    def parse_function(self, func_name, definition):
        func = nodes.FunctionCall(func_name)
        func.definition = definition
        self.add_action(func, grouped=True)

    def parse_open_grouping_token(self, tok):
        if self.parsed_tokens and isinstance(self.parsed_tokens[-1], tokens.WordToken):
            # opening paren of a function call, okay to ignore
            return
        root_action = nodes.RootAction()
        self.add_action(root_action, grouped=True)
        del self.grouping_delimiter_flags[root_action]        

    def parse_closing_grouping_token(self, tok):
        self.pop_grouped_action(tok)

    def parse_open_keysequence_token(self, tok):
        self.add_action(nodes.KeySequence(), grouped=True)

    def parse_number_token(self, tok):
        number_action = nodes.NumberNode(tok.number)
        self.add_action(number_action)

    def pop_grouped_action(self, tok):
        if len(self.grouped_action_stack) < 2:
            self.croak('Too many closing grouping characters')
        last_action = self.grouped_action_stack[-1]
        if isinstance(tok, tokens.KeySequenceClosingToken) and not isinstance(last_action, nodes.KeySequence):
            self.croak('Closing token mismatch')
        print(tok, self.grouped_action_stack[-1])
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

    def croak(self, msg):
        raise RuntimeError(f'Error parsing action "{self.stream.stream.text}":\n{msg}')

    def next(self):
        return self.stream.next()

    def peek(self):
        return self.stream.peek()

    def eof():
        return self.peek() is None

    def parse_positional_variable_token(self, tok):
        var_action = nodes.PositionalVariable(tok.pos)
        self.add_action(var_action)

    def parse_named_variable_token(self, tok):
        var_action = nodes.Argument(tok.name)
        self.add_action(var_action)
        
    def parse_literal_token(self, tok):
        literal_action = nodes.LiteralKeysAction(tok.text)
        self.add_action(literal_action)

    def parse_literal_template_token(self, tok):
        literal_action = nodes.LiteralKeysAction(tok.text, is_template=True)
        self.add_action(literal_action)

    def add_action(self, action, grouped=False):
        if self.append_modifier_flag:
            # _, currently just for repeat 
            self.action_to_modify.modifiers.append(action)
            self.append_modifier_flag = False
        else:
            self.set_delimiter_flag()
            self.grouped_action_stack[-1].add(action)
        if grouped:
            self.grouped_action_stack.append(action)
            self.grouping_delimiter_flags[action] = False
        self.action_to_modify = action 

    def set_delimiter_flag(self):
        # if top level action is expecting a delimiter (, or +), raise an error
        last_action = self.grouped_action_stack[-1]
        if last_action in self.grouping_delimiter_flags:
            if self.grouping_delimiter_flags[last_action]:
                self.croak('Delimiter issuse')
            self.grouping_delimiter_flags[last_action] = True

    def parse_whitespace_token(self, tok):
        return nodes.WhitespaceNode(tok.text)
    
    def parse_underscore_token(self, tok):
        self.append_modifier_flag = True

    def parse_slice_token(self, tok):
        from sprecgrammars import api
        slice_actions = [0, None, 1]
        for i, action_text in enumerate(tok.pieces):
            if not action_text:
                continue
            slice_actions[i] = api.action(action_text, self.defined_functions)
        is_single = len(tok.pieces) == 1
        action_slice = ActionSlice(slice_actions, is_single)
        self.action_to_modify.slices.append(action_slice)

class ActionSlice:

    def __init__(self, slice_actions, is_single):
        assert len(slice_actions) == 3
        self.slice_actions = slice_actions
        self.is_single = is_single

    def apply(self, sliceable, variables, arguments):
        slice_pieces = [a.evaluate(variables, arguments) if isinstance (a, nodes.Action) else a for a in self.slice_actions]
        slice_pieces = [a if a is None else int(a) for a in slice_pieces]
        if self.is_single:
            return sliceable[slice_pieces[0]]
        sliceobj = slice(*slice_pieces)
        return sliceable[sliceobj]
        