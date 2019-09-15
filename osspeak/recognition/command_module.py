import collections
import re
import importlib
import itertools
import json
import lark.exceptions

from recognition.actions.library import history, window
from recognition.actions import variables
from recognition.actions.function import Function
import recognition.actions.astree
import recognition.actions.context
import recognition.rules.astree
from recognition import action as _action, rule as _rule, function, lark_parser
from log import logger

class CommandModule:

    def __init__(self, config):
        self.config = config
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
            try:
                lark_ir = lark_parser.parse_action(action_text)
            except lark.exceptions.UnexpectedCharacters as e:
                action_from_lark = None
            else:
                action_from_lark = recognition.actions.astree.action_from_lark_ir(lark_ir, action_text)
            cmd = Command(rule, rule_text, action, action_text, action_from_lark)
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

    def is_active(self, current_window: str):
        test_fn = self.functions.get('is_active')
        if test_fn:
            context = recognition.actions.context.empty_recognition_context()
            eval_result = test_fn.action.evaluate(context)
            if isinstance(eval_result, str):
                current_window_matches = re.search(eval_result, current_window, flags=re.IGNORECASE)
                return current_window_matches
            return bool(eval_result)
        return True

class Command:
    
    def __init__(self, rule, rule_text, _action, action_input, action):
        self.rule = rule
        self.rule_text = rule_text
        self._action = _action
        self.action_input = action_input
        self.action = action

def command_module_from_lark_ir(module_ir, text_by_line):
    cmd_module = CommandModule({})
    for child in module_ir.children:
        ir_type = lark_parser.lark_node_type(child)
        if ir_type == 'command':
            utterance_ir, action_ir = child.children 
            utterance_text = lark_parser.lark_node_text(utterance_ir, text_by_line)
            utterance = recognition.rules.astree.rule_from_lark_ir(utterance_ir)
            action_text = lark_parser.lark_node_text(action_ir, text_by_line)
            action = recognition.actions.astree.action_from_lark_ir(action_ir, action_text)
            cmd = Command(utterance, utterance_text, action, action_text, action)
            cmd_module.commands.append(cmd)
        elif ir_type == 'function_definition':
            func = recognition.actions.astree.function_definition_from_lark_ir(child)
            cmd_module.functions[func.name] = func

    return cmd_module