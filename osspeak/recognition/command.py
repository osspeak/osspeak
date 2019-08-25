# import recognition.action 
import recognition.utterance

class Command:

    def __init__(self, ast):
        utterance, action = self.parse_ast(ast)
        self.utterance = utterance

    def parse_ast(self, ast):
        assert len(ast.children) == 2
        assert ast.children[0].data == 'utterance'
        utterance = recognition.utterance.Utterance(ast.children[0])
        return None, None