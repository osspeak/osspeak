import os
import unittest

from recognition.actions import pyexpr
from recognition import api
from tests.recognition.actions import strings

class TestPyExpr(unittest.TestCase):

    def parse_action_string(self, action_string):
        return pyexpr.compile_python_expressions(action_string)[0]

    def test_variable1(self):
        exprs = self.parse_action_string(strings.VARIABLE1)
        self.assertEqual(exprs, ['"hello" ', 'context.var(0) ', '"world"'])

    def test_variable2(self):
        exprs = self.parse_action_string(strings.VARIABLE2)
        self.assertEqual(exprs, ['len(context.var(0), context.var(-2))'])

    def test_variable3(self):
        exprs = self.parse_action_string(strings.VARIABLE3)
        self.assertEqual(exprs, ['len(context.var(0), context.var(-2)) ', '"foo $2"'])
