import os
import unittest

from recognition.actions import nodes, tokens, parser, pyexpr
from recognition import api
from tests.recognition.actions import strings

class TestPyExpr(unittest.TestCase):

    def parse_action_string(self, action_string):
        return pyexpr.compile_python_expressions(action_string)

    def test_variable1(self):
        exprs = self.parse_action_string(strings.VARIABLE1)
        self.assertEqual(exprs, ['"hello" ', 'result.vars.get(0) ', '"world"'])

    def test_variable2(self):
        exprs = self.parse_action_string(strings.VARIABLE2)
        self.assertEqual(exprs, ['len(result.vars.get(0), result.vars.get(-2))'])

    def test_variable3(self):
        exprs = self.parse_action_string(strings.VARIABLE3)
        self.assertEqual(exprs, ['len(result.vars.get(0), result.vars.get(-2)) ', '"foo $2"'])
