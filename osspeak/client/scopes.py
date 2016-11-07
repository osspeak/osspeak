from sprecgrammars.formats.rules import astree

class Scope:

    def __init__(self):
        self.cmd_modules = {}
        self.grammar_node = astree.GrammarNode()
        self.grammar_xml = None
        self.variables = {}
        self.functions = {}
    