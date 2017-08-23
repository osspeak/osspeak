import collections
import itertools
import json

from sprecgrammars.actions import nodes
from sprecgrammars.functions.parser import FunctionDefinitionParser
from sprecgrammars.functions.library import state, history
from sprecgrammars import api
from interfaces.gui import serializer
from client import commands, scopes, variables, action
from sprecgrammars.rules import astree
from sprecgrammars.rules.parser import RuleParser
from log import logger

class CommandModule:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.scope = None
        self.rules = []
        self.functions = []
        self.commands = []
        # currently activate and deactivate
        self.events = {}

    def load_commands(self):
        for rule_text, action_text in self.config.get('commands', {}):
            cmd = Command(rule_text, action_text, scope=self.scope)
            self.commands.append(cmd)

    def initialize_rules(self):
        for rule_name, rule_text in self.config.get('rules', {}):
            self.scope.rules[rule_name] = rule_text

    def load_rules(self):
        for rule_name, rule_text in self.config.get('rules', {}):
            current_rule = self.scope.rules[rule_name]
            if isinstance(current_rule, astree.Rule):
                assert current_rule.name is not None
                self.rules.append(current_rule)
                continue
            assert isinstance(current_rule, str)
            self.scope.rules[rule_name] = None
            rule = api.rule(rule_text, name=rule_name, rules=self.scope.rules, defined_functions=self.scope.functions)
            self.scope.rules[rule_name] = rule
            self.rules.append(rule)

    def define_functions(self):
        for func_signature, func_text in self.config.get('functions', {}):
            func_definition = api.func_definition(func_signature, defined_functions=self.scope.functions)
            self.scope.functions[func_definition.name] = func_definition
            self.functions.append(func_definition)

    def set_function_actions(self):
        config_funcs = self.config.get('functions', {})
        for i, func in enumerate(self.functions):
            action_text = config_funcs[i][1]
            func.action = api.action(action_text, defined_functions=self.scope.functions)

    def load_events(self):
        for event_name, event_text in self.config.get('events', {}).items():
            self.events[event_name] = api.action(event_text, defined_functions=self.scope.functions)

    @property
    def conditions(self):
        return self.config.get('conditions', {})

    @property
    def initial_state(self):
        return self.config.get('initialState', {})

    def state_active(self, user_state):
        return 'state' not in self.conditions or eval(self.conditions['state'], {}, user_state)

class Command:
    
    def __init__(self, rule_text, action_text, scope=None):
        self.scope = scopes.Scope() if scope is None else scope
        self.init_rule(rule_text)
        self.init_action(action_text)

    def init_rule(self, rule_text):
        self.rule_text = rule_text
        self.rule = api.rule(rule_text, rules=self.scope.rules)

    def init_action(self, action_text):
        self.action_text = action_text
        self.action = api.action(action_text, self.scope.functions)