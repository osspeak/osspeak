import uuid
from typing import List, Dict
from parsimonious.grammar import Grammar
from recognition.rules import astree, _lark

class GrammarContext:
    
    def __init__(self, xml, command_contexts, active_commands, namespace, named_rules, node_ids):
        self.xml = xml
        self.uuid = str(uuid.uuid4())
        self.command_contexts = command_contexts
        self.active_commands = active_commands 
        self.namespace = namespace
        self.named_rules = named_rules
        self.node_ids = node_ids

        self.command_rules = [cmd.rule for cmd in active_commands]
        self.rule_to_command_map = {c.rule: c for c in active_commands}
        self.lark_grammar = _lark.create_lark_grammar(
            self.command_rules, self.named_rules, self.node_ids)
