import uuid
from typing import List, Dict
from lark import Lark
from recognition.rules import astree

def build_repeat(node):
    if node.repeat_low == 1 and node.repeat_high == 1:
        return ''
    low = node.repeat_low
    high = 99 if node.repeat_high is None else node.repeat_high 
    return f'~{low}' if low == high else f'~{low}..{high}'

def parse_word(node: astree.WordNode, internal_rules, node_ids):
    lark_text = f'"{node.text}"{build_repeat(node)}'
    return lark_rule_if_necessary(node, lark_text, internal_rules, node_ids)

def parse_rule_reference(node: astree.RuleReference, internal_rules, node_ids):
    lark_text = f'{node.rule_name}{build_repeat(node)}'
    return lark_rule_if_necessary(node, lark_text, internal_rules, node_ids)


def lark_rule_if_necessary(node, parsed_text, internal_rules, node_ids):
    has_action_substitute = getattr(node, 'action_substitute', None) is not None
    is_ambiguous_grouping = isinstance(node, astree.GroupingNode) and len(node.sequences) > 1
    is_variable = has_action_substitute or is_ambiguous_grouping
    if is_variable:
        node_id = node_ids[node]
        internal_rules[node_id] = parsed_text
        return node_id
    else:
        return parsed_text

def parse_rule(node, internal_rules, node_ids):
    lark_text = parse_grouping(node.root, internal_rules, node_ids)
    return lark_text

def parse_grouping(node: astree.GroupingNode, internal_rules, node_ids):
    sequences = []
    for seq in node.sequences:
        sequence_items = []
        for node in seq:
            seq_text = wtf[type(node)](node, internal_rules, node_ids)
            sequence_items.append(seq_text)
        joined_items = ' '.join(sequence_items)
        need_parens = len(sequence_items) > 1
        sequences.append(f"({joined_items})" if need_parens else joined_items)
    repeat = build_repeat(node)
    need_parens = len(sequence_items) > 1
    joined_sequences = ' | '.join(sequences)
    lark_text = (f"({joined_sequences})" if need_parens else joined_sequences) + repeat
    return lark_rule_if_necessary(node, lark_text, internal_rules, node_ids)
        # seq.

wtf = {
    astree.GroupingNode: parse_grouping,
    astree.WordNode: parse_word,
    astree.RuleReference: parse_rule_reference
}

def create_lark_grammar(command_rules, named_rules, node_ids):
    lark_rules = create_lark_grammar_list(command_rules, named_rules, node_ids)
    # text = '\n'.join([f'{rule_name} = {rule_text}' for rule_name, rule_text in lark_rules.items()])
    # return Lark(text)

def create_lark_grammar_list(command_rules: List, named_rules, node_ids):
    lark_named_rules = {}
    lark_command_rules = {}
    lark_internal_rules = {}
    print('nr', named_rules)
    for rule in named_rules.values():
        lark_named_rules[node_ids[rule]] = parse_rule(rule, lark_internal_rules, node_ids)
    for rule in command_rules:
        lark_command_rules[node_ids[rule]] = parse_rule(rule, lark_internal_rules, node_ids)
    return [(k, v) for k, v in {**lark_named_rules, **lark_command_rules, **lark_internal_rules}.items()]
