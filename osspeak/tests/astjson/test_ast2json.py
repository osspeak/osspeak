import ast
import os
import unittest
import json

from astjson import ast2json

class TestAST2JSON(unittest.TestCase):

    def test_number(self):
        self.compare('4', {'_type': 'Expression', 'body': {'_type': 'Num', 'col_offset': 0, 'lineno': 1, 'n': 4}})
        
    def test_binop(self):
        self.compare('4 + 7', {
            '_type': 'Expression',
            'body': {
                '_type': 'BinOp',
                'col_offset': 0,
                'left': {
                    '_type': 'Num', 'col_offset': 0, 'lineno': 1, 'n': 4
                },
                'lineno': 1,
                'op': {'_type': 'Add'},
                'right': {
                    '_type': 'Num', 'col_offset': 4, 'lineno': 1, 'n': 7
                }
            }
        })

    # def test_str(self):
    #     self.compare('"hello"', {'body': {'col_offset': 0, 'left': {'col_offset': 0, 'lineno': 1, 'n': 4}, 'lineno': 1, 'op': {}, 'right': {'col_offset': 4, 'lineno': 1, 'n': 7}}})

    def compare(self, s, ast_dict, mode='eval'):
        node = ast.parse(s, mode='eval')
        json_str = json.dumps(node, cls=ast2json.ASTToJSONEncoder)
        node_dict = json.loads(json_str)
        print(node_dict)
        self.assertEqual(node_dict, ast_dict)
