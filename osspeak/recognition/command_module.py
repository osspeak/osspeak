import collections
import re
import importlib
import itertools
import json
import lark.exceptions

from recognition.actions.library import history, window
from recognition.actions import variables
from recognition import cache
import recognition.actions.astree_constructor
import recognition.actions.context
import recognition.rules.astree
from recognition import action as _action, rule as _rule, function, lark_parser
from log import logger

class CommandModule:

    def __init__(self):
        self.named_utterances = {}
        self.functions = {}
        self.commands = []
        # currently activate and deactivate
        self.events = {}

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
    
    def __init__(self, utterance, utterance_text, action_text, action):
        self.utterance = utterance
        self.utterance_text = utterance_text
        self.action_text = action_text
        self.action = action

def command_module_from_lark_ir(module_ir, text_by_line):
    cmd_module = CommandModule()
    for child in module_ir.children:
        ir_type = lark_parser.lark_node_type(child)
        if ir_type == 'command':
            utterance_ir, action_ir = child.children 
            utterance_text = lark_parser.lark_node_text(utterance_ir, text_by_line)
            utterance = recognition.rules.astree.utterance_from_lark_ir(utterance_ir)
            action_text = lark_parser.lark_node_text(action_ir, text_by_line)
            action = recognition.actions.astree_constructor.action_from_lark_ir(action_ir, action_text)
            cmd = Command(utterance, utterance_text, action_text, action)
            cmd_module.commands.append(cmd)
        elif ir_type == 'function_definition':
            func = recognition.actions.astree_constructor.function_definition_from_lark_ir(child)
            cmd_module.functions[func.name] = func
        elif ir_type == 'named_utterance':
            name = str(lark_parser.find_type(child, 'utterance_name').children[0])
            utterance_ir = lark_parser.find_type(child, 'utterance')
            utterance = recognition.rules.astree.utterance_from_lark_ir(utterance_ir)
            cmd_module.named_utterances[name] = utterance
    return cmd_module