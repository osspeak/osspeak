from sprecgrammars.rules import astree
from platforms import api

class Scope:

    def __init__(self, global_scope=None, name=''):
        self.cmd_modules = {}
        self.name = name
        self._rules = {}
        self._functions = {}
        self.global_scope = global_scope

    @property
    def rules(self):
        rules = {} if self.global_scope is None else self.global_scope._rules.copy()
        rules.update(self._rules)
        return rules

    @property
    def functions(self):
        functions = {} if self.global_scope is None else self.global_scope._functions.copy()
        functions.update(self._functions)
        return functions    

class CurrentCondition:

    def __init__(self):
        self.window_title = ''
        self.variables = {}