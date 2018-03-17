import uuid
from typing import List, Dict
from parsimonious.grammar import Grammar
from recognition.rules import astree

def create_parsimonious_grammar(command_rules, named_rules, node_ids):
    parsimonious_rules = create_parsimonious_grammar_dict(command_rules, named_rules, node_ids)
    text = '\n'.join([f'{rule_name} = {rule_text}' for rule_name, rule_text in parsimonious_rules.items()])
    return Grammar(text)

def create_parsimonious_grammar_dict(command_rules: List, named_rules, node_ids):
    parsimonious_rules = {}
    for i, cmd_rule in enumerate(command_rules, start=1):
        
        print(cmd_rule)
    return parsimonious_rules