# from recognition import lark_parser
# import json
# import time

# def rule(text):
#     from recognition.rules.parser import RuleParser
#     from recognition.rules import astree
#     parser = RuleParser(text)
#     rule_obj = parser.parse_as_rule()
#     try:
#         lark_ast = lark_parser.parse_utterance(text)
#     except Exception as e:
#         print(e)
#         print(text)
#     # print(lark_ast.pretty())
#     # print(text)
#     # rule_obj_from_lark = astree.utterance_from_lark_ir(lark_ast)
#     # try:
#     #     assert rule_obj == rule_obj_from_lark
#     # except AssertionError as e:
#     #     with open('larkParser.json', 'w') as f:
#     #         json.dump(rule_obj_from_lark, f, cls=astree.RuleEncoder, sort_keys=True, indent=4)
#     #     with open('handrolledParser.json', 'w') as f:
#     #         json.dump(rule_obj, f, cls=astree.RuleEncoder, sort_keys=True, indent=4)
#     #     raise e
#     return rule_obj

# def action(action_input, *args, **kwargs):
#     from recognition.actions.action import Action
#     action_pieces = input_to_action_pieces(action_input)
#     return Action(action_pieces)

# def function(func_signature, action_input):
#     from recognition.actions.function import Function
#     func = Function(func_signature, action_input)
#     return func

# def input_to_action_pieces(action_input):
#     from recognition.actions import piece
#     if not isinstance (action_input, list):
#         action_input = [action_input]
#     action_objects = [{'type': 'dsl', 'value': x} if isinstance(x, str) else x for x in action_input]
#     action_pieces = [piece.ActionPiece.from_object(obj) for obj in action_objects]
#     return action_pieces