import functools
from lark import Lark, Transformer, v_args, Token, Tree

UTTERANCE_CHOICES = 'utterance_choices'
UTTERANCE_CHOICES_OPTIONAL = 'utterance_choices_optional'
UTTERANCE_CHOICE_ITEMS = 'utterance_choices_items'
UTTERANCE_WORD = 'UTTERANCE_WORD'
IGNORE_AMBIGUITIES = 'IGNORE_AMBIGUITIES'
UTTERANCE_REFERENCE = 'utterance_reference'
UTTERANCE_REPETITION = 'utterance_repetition'
UTTERANCE_RANGE = 'utterance_range'
UTTERANCE_NAME = 'utterance_name'
ACTION_SUBSTITUTE = 'action_substitute'

ZERO_OR_POSITIVE_INTEGER = 'ZERO_OR_POSITIVE_INTEGER'

EXPR = 'expr'
EXPR_SEQUENCE = 'expr_sequence'
EXPR_SEQUENCE_SEPARATOR = 'EXPR_SEQUENCE_SEPARATOR'
SLICE_SEPARATOR = 'SLICE_SEPARATOR'
VARIABLE = 'variable'
ARG_LIST = 'arg_list'
KWARG_LIST = 'kwarg_list'
UNARY_OPERATOR = 'UNARY_OPERATOR'
ARGUMENT_REFERENCE = 'argument_reference'
SLICE = 'slice'

grammar = f'''start: ([_block] _NEWLINE)* [_block]
_block: (command | function_definition | named_utterance | comment | priority)
comment: /[ \t]*#.*/
_WS: /[ \t]/
WS: /[ \t]/
NO_WS_AHEAD: /(?![ \t])/
NO_WS_BEHIND: /(?<![ \t])/

_NEWLINE: /\\n/
NAME: /[_a-zA-Z][_a-zA-Z0-9]*/
named_utterance: {UTTERANCE_NAME} ":=" utterance
utterance: {UTTERANCE_CHOICE_ITEMS} 
utterance_sequence: utterance_piece (_WS+ utterance_piece)*
utterance_piece.-101: ({UTTERANCE_WORD} | {UTTERANCE_REFERENCE} | {UTTERANCE_CHOICES} | {UTTERANCE_CHOICES_OPTIONAL}) [{UTTERANCE_REPETITION}] [{ACTION_SUBSTITUTE}]
{UTTERANCE_CHOICES_OPTIONAL}: [{IGNORE_AMBIGUITIES}] "[" {UTTERANCE_CHOICE_ITEMS} "]"
{UTTERANCE_CHOICES}: [{IGNORE_AMBIGUITIES}] "(" {UTTERANCE_CHOICE_ITEMS} ")"
{UTTERANCE_CHOICE_ITEMS}: utterance_sequence ("|" utterance_sequence)* 
{UTTERANCE_NAME}: NAME
{UTTERANCE_WORD}: /[a-z0-9]+/
{UTTERANCE_REFERENCE}: [{IGNORE_AMBIGUITIES}] "<" {UTTERANCE_NAME} ">"
{ACTION_SUBSTITUTE}: "=" _action
!{UTTERANCE_REPETITION}: (("_" ({ZERO_OR_POSITIVE_INTEGER} | {UTTERANCE_RANGE})) | "*" | "?" | "+")
{UTTERANCE_RANGE}: {ZERO_OR_POSITIVE_INTEGER} "-" [{ZERO_OR_POSITIVE_INTEGER}]
{IGNORE_AMBIGUITIES}: "_" NO_WS_AHEAD
COMPARE_OPERATOR: ("==" | "!=" | "<=" | ">=" | "<"  | ">")
ADDITIVE_OPERATOR: ("+" | "-")
MULTIPLICATIVE_OPERATOR: ("*" | "/" | "//" | "%")

command: utterance "=" _action 

_action: {EXPR}
_grouping: "(" {EXPR} ")"
loop: {EXPR} _LOOP_SEPARATOR {EXPR}
{EXPR_SEQUENCE_SEPARATOR}: /[ \t]+/
{EXPR_SEQUENCE}.-99: _atom_entry ({EXPR_SEQUENCE_SEPARATOR} _atom_entry)+
{EXPR}: _atom_entry | {EXPR_SEQUENCE}
_atom_entry: compare
?compare: or (COMPARE_OPERATOR or)*
?or: and ("||" and)*
?and: not ("&&" not)*
?not: [NOT_OPERATOR] additive
?additive: multiplicative (ADDITIVE_OPERATOR multiplicative)*
?multiplicative: unary (MULTIPLICATIVE_OPERATOR unary)*
?unary: [{UNARY_OPERATOR}] exponent
?exponent: _atom ("**" _atom)*
_atom: (index | {SLICE} | loop | _grouping | attribute | literal | list | STRING_SINGLE | STRING_DOUBLE | REGEX | keypress | {ZERO_OR_POSITIVE_INTEGER} | ZERO_OR_POSITIVE_FLOAT | {VARIABLE} | call | {ARGUMENT_REFERENCE})
_chainable: (NAME | attribute | call | list | {VARIABLE} | {ARGUMENT_REFERENCE} | index | {SLICE})
{UNARY_OPERATOR}: ("+" | "-")
NOT_OPERATOR: "!"
keypress: "{{" {EXPR} "}}"
_VAR_PREC: "$" NO_WS_AHEAD
_LOOP_SEPARATOR: NO_WS_BEHIND "~" NO_WS_AHEAD
_ATTR_SEPARATOR: NO_WS_BEHIND "." NO_WS_AHEAD
_SUBSCRIPT_PREFIX: NO_WS_BEHIND "["
SLICE_SEPARATOR: ":"
_CALL_START: NO_WS_BEHIND "("
{VARIABLE}: _VAR_PREC INTEGER
{ARGUMENT_REFERENCE}: _VAR_PREC NAME
ZERO_OR_POSITIVE_FLOAT: /([0-9]*[.])+[0-9]+/
{ZERO_OR_POSITIVE_INTEGER}: /[0-9]+/
INTEGER: /-?[0-9]+/
LITERAL_PIECE: /[a-zA-Z0-9_]+/ 
literal.-100: LITERAL_PIECE (WS+ LITERAL_PIECE)*

list: "[" [{EXPR} ("," {EXPR})*] "]"
index: _chainable _SUBSCRIPT_PREFIX {EXPR} "]"
{SLICE}: _chainable _SUBSCRIPT_PREFIX [{EXPR}] SLICE_SEPARATOR [{EXPR}] [SLICE_SEPARATOR [{EXPR}]] "]"
attribute: _chainable  _ATTR_SEPARATOR NAME
call: _chainable _CALL_START (({ARG_LIST} ["," {KWARG_LIST}]) | [{KWARG_LIST}]) ")"
{ARG_LIST}: {EXPR} ("," {EXPR})*
{KWARG_LIST}: kwarg ("," kwarg)* 
kwarg: NAME "=" {EXPR}

function_definition: NAME "(" [positional_parameters] ")" "=>" _action
positional_parameters: NAME ("," NAME)*

priority: "priority" ":" {EXPR}

_STRING_INNER: /.*?/
_STRING_ESC_INNER: _STRING_INNER /(?<!\\\\)(\\\\\\\\)*?/ 
STRING_SINGLE: "'" _STRING_ESC_INNER "'"
STRING_DOUBLE: "\\"" _STRING_ESC_INNER "\\""
REGEX: "/" _STRING_ESC_INNER "/"

%import common.WORD  // imports from terminal library
%ignore " "
'''


lark_grammar = Lark(grammar, propagate_positions=True, maybe_placeholders=True, ambiguity='explicit')
utterance_grammar = Lark(grammar, start='utterance', propagate_positions=True, maybe_placeholders=True, ambiguity='explicit')
action_grammar = Lark(grammar, start='_action', propagate_positions=True, maybe_placeholders=True, ambiguity='explicit')


def parse_command_module(text: str):
    ir = lark_grammar.parse(text)
    return ResolveAmbiguities().transform(ir)
    
def parse_utterance(text: str):
    ir = utterance_grammar.parse(text)
    return ResolveAmbiguities().transform(ir)

def parse_action(text: str):
    ir = action_grammar.parse(text)
    return ResolveAmbiguities().transform(ir.children[0])

class ResolveAmbiguities(Transformer):

    resolve_priorities = {node_type: -i for i, node_type in enumerate((EXPR_SEQUENCE, 'literal', 'utterance_piece'), start=1)}

    def _ambig(self, children):
        print('--------------')
        for child in children:
            print(child.pretty())
        compare_fn = functools.cmp_to_key(self.compare_nodes)
        result = min(children, key=compare_fn)
        print(result.pretty())
        return result
        idx = self.find_highest_priority_option_index(children)
        return children[idx]

    def find_highest_priority_option_index(self, nodes):
        max_priority = None
        max_priority_indices = []
        for i, node in enumerate(nodes):
            node_type = lark_node_type(node)
            priority = self.resolve_priorities.get(node_type, 0)
            if max_priority is None or priority > max_priority:
                max_priority_indices = []
                max_priority = priority
            if priority == max_priority:
                max_priority_indices.append(i)
        assert max_priority_indices
        if len(max_priority_indices) == 1:
            return max_priority_indices[0]
        max_priority_options = [nodes[i] for i in max_priority_indices]
        max_index = self.handle_ambig_cases(max_priority_options)
        return max_priority_indices[max_index]

    def handle_ambig_cases(self, options):
        node_types = set(lark_node_type(x) for x in options)
        if len(node_types) == 1:
            node_type = list(node_types)[0]
            if node_type == 'expr_sequence':
                return self.fewest_children(options)
            if node_type == 'utterance_sequence':
                return self.fewest_children(options)
            if node_type == 'unary' and len(options) == 2:
                if options[0].children[0] is None:
                    return 0
                else:
                    return 1
            if node_type == 'expr':
                expr_children = [expr.children[0] for expr in options]
                highest_child = self.find_highest_priority_option_index(expr_children)
                return highest_child
        for i, child in enumerate(options):
            with open(f'{i}.txt', 'w') as f:
                f.write(child.pretty())
        raise RuntimeError('Unresolved ambiguity')

    def compare_nodes(self, a, b):
        a_info = self.node_info(a)
        b_info = self.node_info(b)
        print(a_info, b_info)   
        for a_score, b_score in zip(a_info, b_info):
            if a_score > b_score:
                return 1
            if b_score > a_score:
                return -1
        for a_child, b_child in zip(getattr(a, 'children', []), getattr(b, 'children', [])):
            cmp = self.compare_nodes(a_child, b_child)
            if cmp:
                return cmp
        return 0
        
    def node_info(self, node):
        priority = self.resolve_priorities.get(node, 0)
        child_length = len(getattr(node, 'children', []))
        is_terminal = not isinstance(node, Tree)
        return priority, child_length, is_terminal

    def fewest_children(self, nodes):
        min_children = nodes.index(min(nodes, key=lambda node: len(node.children)))
        return min_children

def lark_node_type(lark_ir):
    type_attr = 'data' if isinstance(lark_ir, Tree) else 'type'
    return getattr(lark_ir, type_attr)

def lark_node_text(lark_ir, text_by_line):
    text = 'foo'
    test_ir = lark_ir
    while test_ir.meta.empty:
        assert len(test_ir.children) == 1
        test_ir = test_ir.children[0]
    start_line, end_line = text_by_line[test_ir.line - 1], text_by_line[test_ir.end_line - 1]
    if test_ir.line == test_ir.end_line:
        text = start_line[test_ir.column - 1:test_ir.end_column - 1]
    return text

def find_type(lark_tree, _type):
    for child in getattr(lark_tree, 'children', []):
        if child is not None:
            child_type_attr = 'data' if isinstance(child, Tree) else 'type'
            child_type = getattr(child, child_type_attr)
            if child_type == _type:
                return child
