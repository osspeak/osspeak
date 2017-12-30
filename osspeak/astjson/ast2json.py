import ast
import json

class ASTToJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if not isinstance(obj, ast.AST):
            return super().default(obj)
        print(obj.__class__.__name__)
        ast_obj = {'_type': obj.__class__.__name__}
        for attr in dir(obj):
            if not attr.startswith('_'):
                val = getattr(obj, attr)
                if isinstance(val, ast.AST):
                    val = self.default(val)
                ast_obj[attr] = val
        return ast_obj
        print(dir(obj))
