import collections
from recognition.rules import astree

class RecognitionResultsTree:

    def __init__(self, root_rule_node, node_ids, named_rule_map):
        self.root_rule_node = root_rule_node
        self.node_ids = node_ids
        self.named_rule_map = named_rule_map
        self.initialize_fields()

    def initialize_fields(self):
        self.node_paths = {}
        possible_variables = []
        for node_wrapper in self.iterate_subtree(self.root_rule_node):
            if self.is_variable(node_wrapper):
                possible_variables.append(node_wrapper)
            self.node_paths[node_wrapper.path] = node_wrapper.node
        self.variables = collections.OrderedDict()
        for wrapper in possible_variables:
            ancestor_is_variable = any(w in possible_variables for w in wrapper.ancestors)
            if not ancestor_is_variable:
                self.variables[wrapper.path] = wrapper.node

    def is_variable(self, node_wrapper):
        for wrapper in node_wrapper.ancestors + (node_wrapper,):
            if getattr(wrapper.node, 'ignore_ambiguities', False):
                return False
        is_grouping_variable = isinstance(node_wrapper.node, astree.GroupingNode) and len(node_wrapper.node.sequences) > 1
        is_dictation = (isinstance(node_wrapper.node, astree.RuleReference) and
                        node_wrapper.node.rule_name == '_dictation')
        multiple_repeat_possibilities = getattr(node_wrapper.node, 'repeat_low', None) != getattr(node_wrapper.node, 'repeat_high', None) 
        is_variable = is_grouping_variable or is_dictation
        return is_variable or multiple_repeat_possibilities

    def iterate_subtree(self, node, ancestors=()):
        wrapper = RuleNodeWrapper(node, ancestors, self.node_ids)
        yield wrapper
        child_ancestors = ancestors + (wrapper,)
        if isinstance(node, astree.GroupingNode):
            for seq in node.sequences:
                for child in seq:
                    yield from self.iterate_subtree(child, child_ancestors)
        elif isinstance(node, astree.RuleReference):
            rule = self.named_rule_map[node.rule_name]
            yield from self.iterate_subtree(rule, child_ancestors)
        elif isinstance(node, astree.Rule):
            yield from self.iterate_subtree(node.root, child_ancestors)

class RuleNodeWrapper:

    def __init__(self, node, ancestors, node_ids):
        self.node = node
        self.ancestors = ancestors
        self.path = tuple([node_ids[wrapper.node] for wrapper in ancestors] + [node_ids[node]])
