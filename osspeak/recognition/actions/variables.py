import collections
from recognition.rules import astree
from recognition.actions.action import Action

class RecognitionResultsTree:

    def __init__(self, root_rule_node, node_ids, named_rule_map):
        self.root_rule_node = root_rule_node
        self.node_ids = node_ids
        self.named_rule_map = named_rule_map
        self.initialize_fields()

    def walk_tree(self):
        for node_info in self.root_rule_node.walk(rules=self.named_rule_map):
            yield RuleNodeWrapper(node_info['node'], node_info['ancestors'], self.node_ids)

    def initialize_fields(self):
        self.node_paths = {}
        self.variables = collections.OrderedDict()
        for node_wrapper in self.iterate_subtree(self.root_rule_node):
            is_grouping_variable = isinstance(node_wrapper.node, astree.GroupingNode) and len(node_wrapper.node.sequences) > 1
            is_dictation = (isinstance(node_wrapper.node, astree.RuleReference) and
                            node_wrapper.node.rule_name == '_dictate')
            is_variable = is_grouping_variable or is_dictation
            if is_variable:
                self.variables[node_wrapper.path] = node_wrapper.node
            self.node_paths[node_wrapper.path] = node_wrapper.node

    def iterate_subtree(self, node, ancestors=()):
        wrapper = RuleNodeWrapper(node, ancestors, self.node_ids)
        yield wrapper
        child_ancestors = ancestors + (node,)
        if isinstance(node, astree.GroupingNode):
            for seq in node.sequences:
                for child in seq:
                    yield from self.iterate_subtree(child, child_ancestors)
        elif isinstance(node, astree.RuleReference):
            rule = self.named_rule_map[node.rule_name]
            yield from self.iterate_subtree(rule, child_ancestors)
        elif isinstance(node, astree.Rule):
            yield from self.iterate_subtree(node.root, child_ancestors)

    def leaf_action(self, node, result_text):
        if getattr(node, 'action_substitute', None) is not None:
            return node.action_substitute
        if isinstance(node, astree.WordNode):
            return Action(f"'{node.text}'")
        if isinstance(node, astree.RuleReference) and node.rule_name == '_dictate':
            return Action(f"'{result_text}'")
        # raise TypeError

    def action_variables(self, lark_tree):
        results = collections.OrderedDict({path: [] for path in self.variables})
        full_path_engine_variables = self.get_full_path_engine_variables(engine_variables)
        # for full_path, action_text in full_path_engine_variables:
        #     action_path_length = len(full_path)
        #     action = self.leaf_action(self.node_map[full_path].node, action_text)
        #     for variable_path in self.variables:
        #         if full_path[:len(variable_path)] == variable_path:
        #             if len(variable_path) < action_path_length:
        #                 node = self.node_map[variable_path].node
        #                 if getattr(node, 'action_substitute', None) is not None:
        #                     action_path_length = len(variable_path)
        #                     action = node.action_substitute
        #             results[variable_path].append(action)
        var_list = list(results.values())
        return var_list

class RuleNodeWrapper:

    def __init__(self, node, ancestors, node_ids):
        self.node = node
        self.ancestors = ancestors
        self.full_path = tuple([node_ids[n] for n in ancestors] + [node_ids[node]])
        self.path = tuple(self.full_path[1:])
        self.path = self.full_path

