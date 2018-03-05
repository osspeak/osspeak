from recognition.rules import astree
from common import binheap
import heapq
from typing import List

class RuleTextMatch:

    def __init__(self, node, start, span):
        self.node = node
        self.start = start
        self.span = span
        
class MatchCollection:

    def __init__(self, matches):
        self.heap = binheap.MaxHeap()
        self.match_map = {}
        self.matches = matches

    def add(self, match: RuleTextMatch):
        match_key = (match.start, match.span)
        if match_key in self.match_map:
            return False
        self.heap.push(match)
        self.match_map[match_key] = match


def match_recognition(words, grammar_context):
    print(words, grammar_context.command_rules)
    rules = grammar_context.command_rules
    seen = {}
    match = match_rules(rules, words, 0, seen)

def match_rules(rules, words, start, seen):
    for rule in rules:
        rule_match = match_rule_node(rule, words, start)
        if rule_match is None:
            continue
        match_key = ()
    else:
        pass
        

def match_rule_node(node: astree.ASTNode, words, start) -> MatchCollection:
    return match_grouping_node(node.root, words, start)

def match_grouping_node(node: astree.ASTNode, words, start) -> MatchCollection:
    pass

def match_word_node(node, words, start):
    pass

def count_repetition(words: List[str], start: int) -> int:
    count = 1
    startval = words[start]
    try:
        while startval == words[start + count]:
            count += 1
    except IndexError:
        pass
    return count


MATCH_FUNCTIONS = {
    astree.WordNode: match_word_node
}


class MaxHeap:

    def __init__(self):
        self._heap = []