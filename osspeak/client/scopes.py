from sprecgrammars.formats.rules import astree
from platforms import api

class Scope:

    def __init__(self, global_scope=None):
        self.cmd_modules = {}
        self._variables = {}
        self._functions = {}
        self.global_scope = global_scope

    @property
    def variables(self):
        variables = {} if self.global_scope is None else self.global_scope._variables.copy()
        variables.update(self._variables)
        return variables

    @property
    def functions(self):
        functions = {} if self.global_scope is None else self.global_scope._functions.copy()
        functions.update(self._functions)
        return functions    

class CurrentCondition:

    def __init__(self):
        self.window_title = api.get_active_window_name()
        self.variables = {}