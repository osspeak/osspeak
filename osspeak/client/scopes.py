from sprecgrammars.formats.rules import astree
from platforms import api

class Scope:

    def __init__(self):
        self.current_window_title = api.get_active_window_name().lower()
        self.cmd_modules = {}
        self.grammar_node = astree.GrammarNode()
        self.grammar_xml = None
        self.variables = {}
        self.functions = {}
