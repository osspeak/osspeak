import collections
import importlib
import itertools
import json

from recognition.actions.library import state, history
from recognition.actions import variables
from recognition import api
from interfaces.gui import serializer
from recognition.commands import scopes
from recognition.rules import astree
from recognition.rules.parser import RuleParser
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

    def import_modules(self):
        for module_name in self.config.get("imports", []):
            self.scope.functions[module_name] = importlib.import_module(module_name)

    def load_commands(self):
        for rule_text, action_text in self.config.get('commands', {}):
            cmd = Command(rule_text, action_text, scope=self.scope)
            self.commands.append(cmd)

    def initialize_rules(self):
        for rule_name, rule_text in self.config.get('rules', {}):
            self.scope.rules[rule_name] = rule_text

    def load_rules(self):
        for rule_name, rule_text in self.config.get('rules', {}):
            rule = api.rule(rule_text, name=rule_name, rules=self.scope.rules, defined_functions=self.scope.functions)
            self.scope.rules[rule_name] = rule
            self.rules.append(rule)

    def define_functions(self):
        for func_signature, func_text in self.config.get('functions', {}):
            user_function = api.function(func_signature, func_text)
            self.scope.functions[user_function.name] = user_function
            self.functions.append(user_function)

    def set_function_actions(self):
        for func in self.functions:
            func.compile_action(self.scope.functions)

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