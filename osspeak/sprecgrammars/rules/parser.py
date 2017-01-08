import copy

from sprecgrammars.rules import ruletokstream, astree, tokens

class RuleParser:
    '''
    Convert a rule string i.e. 'hello (world|universe) into
    an abstract syntax tree of nodes that can be serialized
    into speech recognition grammar formats like SRGS XML. 
    '''

    def __init__(self, text, rules=None, debug=False):
        self.text = text
        self.rules = {} if rules is None else rules
        self.debug = debug
        self.stream = ruletokstream.RuleTokenStream(self.text)
        self.grouping_stack = []
        self.token_list = []
        self.parse_map = {
            tokens.WordToken: self.parse_word_token,
            tokens.OrToken: self.parse_or_token,
            tokens.GroupingOpeningToken: self.parse_grouping_opening_token,
            tokens.GroupingClosingToken: self.parse_grouping_closing_token,
            tokens.RepetitionToken: self.parse_repetition_token,
            tokens.NamedRuleToken: self.parse_named_rule_token,
            tokens.ActionSubstituteToken: self.parse_action_substitute_token
        }

    def parse_as_rule(self, name=None):
        top_level_rule = astree.Rule(name=name)
        self.grouping_stack = [top_level_rule]
        for tok in self.stream:
            self.token_list.append(tok)
            self.parse_map[type(tok)](tok)
        assert len(self.grouping_stack) == 1 and self.grouping_stack[0] is top_level_rule
        return top_level_rule

    def parse_word_token(self, tok):
        self.pop_top_grouping_if_closed()
        word_node = astree.WordNode(tok.text)
        self.top.children.append(word_node)

    def parse_or_token(self, tok):
        self.pop_top_grouping_if_closed()
        or_node = astree.OrNode()
        self.top.children.append(or_node)

    def parse_named_rule_token(self, tok):
        from sprecgrammars import api
        self.pop_top_grouping_if_closed()
        rule_node = self.rules[tok.name]
        # rule text -> None -> Rule object
        if isinstance(rule_node, str):
            # rule node is currently rule text
            self.rules[tok.name] = None
            rule_node = api.rule(rule_node, name=tok.name, rules=self.rules)
            self.rules[tok.name] = rule_node
        # want a copy to avoid mutating original, ie repeat
        rule_copy = copy.copy(rule_node)
        self.grouping_stack[0].groupings.update(rule_copy.groupings)
        if rule_copy.name == '_dictate':
            self.grouping_stack[0].groupings[rule_copy.id] = None
        self.top.children.append(rule_copy)

    def parse_grouping_opening_token(self, tok):
        self.pop_top_grouping_if_closed()
        grouping_node = astree.GroupingNode()
        self.top.children.append(grouping_node)
        self.grouping_stack.append(grouping_node)

    def parse_grouping_closing_token(self, tok):
        self.top.open = False
        self.pop_top_grouping_if_closed()

    def parse_repetition_token(self, tok):
        repeated_node = self.modifiable_node
        repeated_node.repeat_low = tok.low
        repeated_node.repeat_high = tok.high

    def parse_action_substitute_token(self, tok):
        self.modifiable_node.action_substitute = tok.action

    def apply_repetition(self, node, low=0, high=None):
        if low is not None:
            node.low = low

    def pop_top_grouping_if_closed(self):
        if not self.top.open:
            grouping = self.grouping_stack.pop()
            self.grouping_stack[0].groupings[grouping.id] = None

    @property
    def top(self):
        return self.grouping_stack[-1]

    @property
    def modifiable_node(self):
        if not self.top.open:
            return self.top
        if self.top.children:
            return self.top.children[-1]
        self.croak('No modifiable rule node exists')