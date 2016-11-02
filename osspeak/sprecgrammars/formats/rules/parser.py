from sprecgrammars import tokens
from sprecgrammars.formats.baseparser import BaseParser
from sprecgrammars.formats.rules import ruletokstream, astree


class RuleParser(BaseParser):
    '''
    Convert a rule string i.e. 'hello (world|universe) into
    an abstract syntax tree of nodes that can be serialized
    into speech recognition grammar formats like SRGS XML. 
    '''

    def __init__(self, text, variables=None):
        super().__init__(text)
        self.variables = {} if variables is None else variables
        self.stream = ruletokstream.RuleTokenStream(self.text)
        self.grouping_stack = []
        self.groupings = []
        self.token_list = []
        self.parse_map = {
            tokens.WordToken: self.parse_word_token,
            tokens.OrToken: self.parse_or_token,
            tokens.ParenToken: self.parse_paren_token,
            tokens.RepetitionToken: self.parse_repetition_token,
            tokens.VariableToken: self.parse_variable_token,
            tokens.ActionSubstituteToken: self.parse_action_substitute_token
        }

    def parse_as_rule(self):
        top_level_rule = astree.Rule()
        self.grouping_stack = [top_level_rule]
        for tok in self.stream:
            self.token_list.append(tok)
            self.parse_map[type(tok)](tok)
        assert len(self.grouping_stack) == 1
        for grouping in self.groupings:
            top_level_rule.grouping_variables[grouping.id] = grouping
            top_level_rule.grouping_variables_empty[grouping.id] = None
            grouping.child_ids = {c.id: c for c in grouping.children}
        return top_level_rule

    def parse_word_token(self, tok):
        self.maybe_pop_top_grouping()
        word_node = astree.WordNode(tok.text)
        self.top.children.append(word_node)

    def parse_or_token(self, tok):
        self.maybe_pop_top_grouping()
        or_node = astree.OrNode()
        self.top.children.append(or_node)

    def parse_variable_token(self, tok):
        self.maybe_pop_top_grouping()
        var_node = self.variables[tok.name]
        self.groupings.extend(list(var_node.rule.grouping_variables.values()))
        self.top.children.append(var_node)

    def parse_paren_token(self, tok):
        self.maybe_pop_top_grouping()
        if tok.is_open:
            grouping_node = astree.GroupingNode()
            self.top.children.append(grouping_node)
            self.grouping_stack.append(grouping_node)
        else:
            self.top.open = False
            self.maybe_pop_top_grouping()

    def parse_repetition_token(self, tok):
        if not self.top.open:
            repeated_node = self.top
        elif self.top.children:
            repeated_node = self.top.children[-1]
        else:
            self.croak('Invalid repetition')
        repeated_node.repeat_low = tok.low
        repeated_node.repeat_high = tok.high

    def parse_action_substitute_token(self, tok):
        if self.top.open:
            self.top.children[-1].action_substitute = tok.action
        else:
            self.top.action_substitute = tok.action

    def apply_repetition(self, node, low=0, high=None):
        if low is not None:
            node.low = low

    def maybe_pop_top_grouping(self):
        if not self.top.open:
            grouping = self.grouping_stack.pop()
            self.groupings.append(grouping)

    @property
    def top(self):
        return self.grouping_stack[-1]