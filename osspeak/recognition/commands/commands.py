import collections
import importlib
import itertools
import json

from recognition.actions.library import state, history
from recognition.actions import variables
from recognition.actions.function import Function
from recognition import action, rule, function
from log import logger

class CommandModule:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.rules = {}
        self.functions = {}
        self.commands = []
        # currently activate and deactivate
        self.events = {}

    def import_modules(self):
        for module_name in self.config.get("imports", []):
            self.functions[module_name] = importlib.import_module(module_name)

    def load_commands(self):
        for rule_text, action_text in self.config.get('commands', {}):
            cmd = Command(rule_text, action_text)
            self.commands.append(cmd)

    def load_rules(self):
        for rule_name, rule_text in self.config.get('rules', {}):
            try:
                self.rules[rule_name] = rule(rule_text, name=rule_name)
            except RuntimeError as e:
                print(f'Error loading rule "{rule_name}": {e}')

    def define_functions(self):
        for func_signature, func_text in self.config.get('functions', {}):
            user_function = function(func_signature, func_text)
            self.functions[user_function.name] = user_function

    def set_function_actions(self):
        for func in self.functions.values():
            if isinstance(func, Function):
                func.compile_action_pieces()

    def load_events(self):
        for event_name, event_text in self.config.get('events', {}).items():
            self.events[event_name] = action(event_text)

    @property
    def conditions(self):
        return self.config.get('conditions', {})

    @property
    def initial_state(self):
        return self.config.get('initialState', {})

    def is_state_active(self, user_state):
        for key, value in self.conditions.get('state', {}).items():
            if key not in user_state or value != user_state[key]:
                return False
        return True

class Command:
    
    def __init__(self, rule_text, action_input):
        self.init_rule(rule_text)
        self.init_action(action_input)

    def init_rule(self, rule_text):
        self.rule_text = rule_text
        self.rule = rule(rule_text)

    def init_action(self, action_input):
        self.action_input = action_input
        self.action = action(action_input)