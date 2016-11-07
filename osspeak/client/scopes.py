from sprecgrammars.formats.rules import astree

class Scope:

    def __init__(self, config):
        self.window_title = config.get('title')
        self.cmd_modules = {}
        self.grammar_node = astree.GrammarNode()
        self.grammar_xml = None
        self.variables = {}
        self.functions = {}

    def config_matches(self, config):
        if config.get('title') != self.window_title:
            return False
        return True
    