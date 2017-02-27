from sprecgrammars.rules import astree
from platforms import api

class Scope:

    def __init__(self, global_scope=None, name=''):
        self.cmd_modules = {}
        self.name = name
        if global_scope is None:
            self.rules = ScopeFieldMap({})
            self.functions = ScopeFieldMap({})
        else:
            self.rules = ScopeFieldMap(global_scope.rules.global_dict, {})
            self.functions = ScopeFieldMap(global_scope.functions.global_dict, {})

class CurrentCondition:

    def __init__(self):
        self.window_title = ''
        self.variables = {}

class ScopeFieldMap:

    def __init__(self, global_dict, local_dict=None):
        self.global_dict = global_dict
        self.local_dict = local_dict

    def __getitem__(self, key):
        if self.local_dict is not None and key in self.local_dict:
            return self.local_dict[key]
        return self.global_dict[key]

    def __setitem__(self, key, val):
        set_dict = self.global_dict if self.local_dict is None else self.local_dict
        set_dict[key] = val

    def __contains__(self, key):
        if self.local_dict is not None and key in self.local_dict:
            return key in self.local_dict
        return key in self.global_dict
    