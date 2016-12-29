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
        self.groupings = []
        self.token_list = []
        self.parse_map = {
            tokens.WordToken: self.parse_word_token,
            tokens.OrToken: self.parse_or_token,
            tokens.ParenToken: self.parse_paren_token,
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
        for grouping in self.groupings:
            top_level_rule.grouping_variables[grouping.id] = grouping
            top_level_rule.grouping_variables_empty[grouping.id] = None
            grouping.child_ids = self.build_child_ids(grouping)
        return top_level_rule

    def build_child_ids(self, grouping):
        child_ids = {}
        for child in grouping.children:
            node = child
            child_ids[node.id] = node
        return child_ids

    def parse_word_token(self, tok):
        self.maybe_pop_top_grouping()
        word_node = astree.WordNode(tok.text)
        self.top.children.append(word_node)

    def parse_or_token(self, tok):
        self.maybe_pop_top_grouping()
        or_node = astree.OrNode()
        self.top.children.append(or_node)

    def parse_named_rule_token(self, tok):
        from sprecgrammars import api
        self.maybe_pop_top_grouping()
        rule_node = self.rules[tok.name]
        # rule text -> None -> Rule object
        if isinstance(rule_node, str):
            # rule node is currently rule text
            self.rules[tok.name] = None
            rule_node = api.rule(rule_node, name=tok.name, rules=self.rules)
            self.rules[tok.name] = rule_node
        # want a copy to avoid mutating original, ie repeat
        rule_copy = copy.copy(rule_node)
        self.groupings.extend(list(rule_copy.grouping_variables.values()))
        self.top.children.append(rule_copy)

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