import os
import unittest

from sprecgrammars.actions import nodes, tokens, parser, pyexpr
from sprecgrammars import api
from tests.sprecgrammars.actions import strings

class TestPyExpr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.function_definitions = {}
        defs = {
            'mouse.click()': '' 
        }
        for sig, action in defs.items():
            func_def = api.func_definition(sig, action)
            cls.function_definitions[func_def.name] = func_def

    def parse_action_string(self, action_string):
        results = pyexpr.compile_python_expressions(action_string)
        return [r[1] for r in results]

    def test_variable1(self):
        exprs = self.parse_action_string(strings.VARIABLE1)
        self.assertEqual(exprs, ['"hello" ', 'variables[0] ', '"world"'])

    def test_variable2(self):
        exprs = self.parse_action_string(strings.VARIABLE2)
        self.assertEqual(exprs, ['len(variables[0], variables[-2])'])

    def test_variable3(self):
        exprs = self.parse_action_string(strings.VARIABLE3)
        self.assertEqual(exprs, ['len(variables[0], variables[-2])', '"foo $2"'])
