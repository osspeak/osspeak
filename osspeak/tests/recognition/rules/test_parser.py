import unittest
import json
from pprint import pprint

from recognition.rules import converter, parser 
from recognition.rules.json import RuleAstEncoder
from recognition.rules.astree import GroupingNode, OrNode, WordNode 
from tests.recognition.rules import strings

class TestRuleParserBase(unittest.TestCase):

    def rule(self, text):
        rule_parser = parser.RuleParser(text)
        ruleobj = rule_parser.parse_as_rule()
        return ruleobj

    def encode_rule(self, rule):
        return json.loads(json.dumps(rule, cls=RuleAstEncoder))
    
    def rule_test(self, text, test_dict):
        rule = self.rule(text)
        json_rule = self.encode_rule(rule)
        # pprint(json_rule)
        self.assertEqual(json_rule, test_dict)

class TestRuleGrouping(TestRuleParserBase):

    def test_simple(self):
        test_dict = {
            'children': [{'children': [{'text': 'hello', 'type': 'word'},
                            {'children': [{'text': 'world', 'type': 'word'},
                                          {'type': 'or'},
                                          {'text': 'universe', 'type': 'word'}],
                             'type': 'grouping'}],
               'type': 'grouping'}],
            'type': 'rule'
        }
        self.rule_test(strings.GROUPING1, test_dict)
        
    def test_substitute(self):
        self.maxDiff = None
        #((dollar sign)='$' | semicolon) 
        test_dict = {
            'children':[
                {'children': [
                    {'children': [
                        {'text': 'dollar', 'type': 'word'},
                        {'text': 'sign', 'type': 'word'}
                    ],
                    'action': "'$' ",
                    'type': 'grouping'},
                    {'type': 'or'},
                    {'text': 'semicolon', 'type': 'word'}
                ],
               'type': 'grouping'}],
            'type': 'rule'
        }
        self.rule_test(strings.SUBSTITUTE4, test_dict)