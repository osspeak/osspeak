class Utterance:

    def __init__(self, ast):
        self.parse_ast(ast)

    def parse_ast(self, ast):
        print(ast.pretty())
        return None, None