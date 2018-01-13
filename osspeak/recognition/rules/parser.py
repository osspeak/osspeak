import copy

from recognition.rules import ruletokstream, astree, tokens
from profile import Profiler

class RuleParser:
    '''
    Convert a rule string i.e. 'hello (world|universe)' into
    an abstract syntax tree of nodes that can be serialized
    into speech recognition grammar formats like SRGS XML. 
    '''

    def __init__(self, text, rules=None, defined_functions=None, debug=False):
        self.text = text
        self.rules = {} if rules is None else rules
        self.debug = debug
        self.stream = ruletokstream.RuleTokenStream(self.text, defined_functions=defined_functions)
        self.grouping_stack = []
        self.optional_groupings = set()
        self.repeated_nodes = set()
        self.token_list = []
        self.parse_map = {
            tokens.WordToken: self.parse_word_token,
            tokens.OrToken: self.parse_or_token,
            tokens.GroupingOpeningToken: self.parse_grouping_opening_token,
            tokens.GroupingClosingToken: self.parse_grouping_closing_token,
            tokens.OptionalGroupingOpeningToken: self.parse_optional_grouping_opening_token,
            tokens.OptionalGroupingClosingToken: self.parse_optional_grouping_closing_token,
            tokens.RepetitionToken: self.parse_repetition_token,
            tokens.NamedRuleToken: self.parse_named_rule_token,
            tokens.ActionSubstituteToken: self.parse_action_substitute_token,
            tokens.WhitespaceToken: self.parse_whitespace_token,
        }

    def parse_as_rule(self, name=None):
        top_level_rule = astree.Rule(name=name)
        self.grouping_stack = [top_level_rule]
        for tok in self.stream:
            self.token_list.append(tok)
            self.parse_map[type(tok)](tok)
        valid_last_grouping = len(self.grouping_stack) == 1 or len(self.grouping_stack) == 2 and not self.grouping_stack[-1].open
        assert self.grouping_stack[0] is top_level_rule and valid_last_grouping
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
        from recognition import api
        self.pop_top_grouping_if_closed()
        rule_reference = astree.RuleReference(tok.name)
        self.top.children.append(rule_reference)

    def parse_named_rule_token(self, tok):
        from recognition import api
        self.pop_top_grouping_if_closed()
        rule_reference = astree.RuleReference(tok.name)
        rule_node = self.rules[tok.name]
        # rule text -> None -> Rule object
        if isinstance(rule_node, str):
            # rule node is currently rule text
            self.rules[tok.name] = None
            rule_node = api.rule(rule_node, name=tok.name, rules=self.rules)
            self.rules[tok.name] = rule_node
        # want a copy to avoid mutating original, ie repeat
        # Need to figure out a way to make unique ids that
        # still point to rulerefs
        rule_copy = rule_node.create_reference()
        self.top.children.append(rule_copy)

    def parse_grouping_opening_token(self, tok):
        self.pop_top_grouping_if_closed()
        grouping_node = astree.GroupingNode()
        self.top.children.append(grouping_node)
        self.grouping_stack.append(grouping_node)

    def parse_grouping_closing_token(self, tok):
        self.pop_top_grouping_if_closed()
        if self.top in self.optional_groupings:
            self.croak("Can't match '[' with ')'")
        self.top.open = False

    def parse_optional_grouping_opening_token(self, tok):
        self.parse_grouping_opening_token(tok)
        self.optional_groupings.add(self.top)
        self.apply_repetition(self.top, 0, 1)

    def parse_optional_grouping_closing_token(self, tok):
        if self.top not in self.optional_groupings:
            self.croak("Can't match '(' with ']'")
        self.pop_top_grouping_if_closed()
        self.top.open = False

    def parse_repetition_token(self, tok):
        repeated_node = self.modifiable_node
        self.apply_repetition(repeated_node, tok.low, tok.high)

    def parse_action_substitute_token(self, tok):
        self.modifiable_node.action_substitute = tok.action

    def parse_whitespace_token(self, tok):
        pass

    def pop_top_grouping_if_closed(self):
        if not self.top.open:
            grouping = self.grouping_stack.pop()

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

    def apply_repetition(self, node, low, high):
        if node in self.repeated_nodes:
            self.croak('Cannot apply repetition to node twice')
        self.repeated_nodes.add(node)
        node.repeat_low = low
        node.repeat_high = high

    def croak(self, message):
        raise RuntimeError(message)