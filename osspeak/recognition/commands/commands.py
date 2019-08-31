import collections
import importlib
import itertools
import json
import lark.exceptions

from recognition.actions.library import state, history
from recognition.actions import variables
from recognition.actions.function import Function
from recognition import action as _action, rule as _rule, function, lark_parser
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
            try:
                lark_parser.parse_utterance(rule_text)
            except Exception as e:
                print(rule_text)
                print(e)
            rule = _rule(rule_text)
            action = _action(action_text)
            # try:
            #     lark_ast = lark_parser.parse_action(action_text)
            # except lark.exceptions.UnexpectedCharacters as e:
            #     print(e)
            #     print(action_text)
            cmd = Command(rule, rule_text, action, action_text)
            self.commands.append(cmd)

    def load_rules(self):
        for rule_name, rule_text in self.config.get('rules', {}):
            try:
                self.rules[rule_name] = _rule(rule_text)
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
            self.events[event_name] = _action(event_text)

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
    
    def __init__(self, r, rule_text, a, action_input):
        self.rule = r
        self.rule_text = rule_text
        self.action = a
        self.action_input = action_input