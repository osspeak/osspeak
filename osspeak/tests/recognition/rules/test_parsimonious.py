import os
import unittest

from recognition.commands import match, loader
from recognition.rules import _parsimonious
from recognition import api
from tests.recognition.actions import strings

class TestParsimonious(unittest.TestCase):

    def grammar_dict(self, command_rules=None, named_rules=None):
        command_rules = [api.rule(text) for text in command_rules] if command_rules else []
        named_rules = [api.rule(text) for text in named_rules] if named_rules else []
        named_rules = {r.name: r for r in named_rules}
        all_rules = list(named_rules.values()) + command_rules
        node_ids = loader.generate_node_ids(all_rules, named_rules)

        print(node_ids)
        return _parsimonious.create_parsimonious_grammar_dict(command_rules, named_rules, node_ids)

    def test_count_repetition(self):
        command_rules = [
            'hello'
        ]
        grammar_dict = self.grammar_dict(command_rules)
        print(grammar_dict)

    def test_count_repetition_non_repeating(self):
        self.assertEqual(match.count_repetition(['this', 'is', 'a', 'test'], 0), 1)