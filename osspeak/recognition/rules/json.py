import json
from recognition.rules import astree

class RuleAstEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, astree.ASTNode):
            obj_dict = getattr(self, f'encode_{obj.__class__.__name__}')(obj)
            if getattr(obj, 'action_substitute', None) is not None:
                obj_dict['action'] = ''.join(obj.action_substitute.literal_expressions)
            return obj_dict
        return super().default(obj)

    def encode_Rule(self, node):
        return {
            'type': 'rule',
            'children': [self.default(c) for c in node.children]
        }

    def encode_GroupingNode(self, node):
        return {
            'type': 'grouping',
            'children': [self.default(c) for c in node.children]
        }

    def encode_WordNode(self, node):
        return {
            'type': 'word',
            'text': node.text
        }
    def encode_OrNode(self, node):
        return {
            'type': 'or'
        }