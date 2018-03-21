import collections
from recognition.rules import astree
from recognition.actions.action import Action

class RecognitionResultsTree:

    def __init__(self, root_rule_node, node_ids, named_rule_map):
        self.root_rule_node = root_rule_node
        self.node_ids = node_ids
        self.named_rule_map = named_rule_map
        # self.initialize_fields()

    def walk_tree(self):
        for node_info in self.root_rule_node.walk(rules=self.named_rule_map):
            yield RuleNodeWrapper(node_info['node'], node_info['ancestors'], self.node_ids)

    def initialize_fields(self):
        self.node_map = {}
        self.variables = []
        for node_wrapper in self.walk_tree():
            is_grouping_variable = isinstance(node_wrapper.node, astree.GroupingNode) and len(node_wrapper.node.children) > 1
            is_dictation = (isinstance(node_wrapper.node, astree.RuleReference) and
                            node_wrapper.node.rule_name == '_dictate')
            is_variable = is_grouping_variable or is_dictation
            if is_variable:
                self.variables.append(node_wrapper.path)
            self.node_map[node_wrapper.path] = node_wrapper

    def get_full_path_engine_variables(self, engine_variables):
        full_path_engine_variables = []
        path = ()
        for i, (var_id, var_val) in enumerate(engine_variables):
            split_id = var_id.split('-', 1)
            if split_id[0] == 'dictation':
                var_id = split_id[1]
            if path not in self.node_map:
                path = ()
                continue
            next_path = path + (var_id,)
            if next_path not in self.node_map:
                action_text = engine_variables[i - 1][1]
                full_path_engine_variables.append((path, action_text))
                next_path = self.next_path(list(path), var_id)
            path = next_path
        if path:
            action_text = engine_variables[-1][1]
            full_path_engine_variables.append((path, action_text))
        return full_path_engine_variables

    def next_path(self, current_path, next_end):
        next_path = []
        while current_path:
            path = tuple(current_path + [next_end])
            if path in self.node_map:
                return path
            current_path.pop()
        return (next_end,)

    def leaf_action(self, node, result_text):
        if getattr(node, 'action_substitute', None) is not None:
            return node.action_substitute
        if isinstance(node, astree.WordNode):
            return Action(f"'{node.text}'")
        if isinstance(node, astree.RuleReference) and node.rule_name == '_dictate':
            return Action(f"'{result_text}'")
        # raise TypeError

    def action_variables(self, engine_variables):
        results = collections.OrderedDict({path: [] for path in self.variables})
        full_path_engine_variables = self.get_full_path_engine_variables(engine_variables)
        for full_path, action_text in full_path_engine_variables:
            action_path_length = len(full_path)
            action = self.leaf_action(self.node_map[full_path].node, action_text)
            for variable_path in self.variables:
                if full_path[:len(variable_path)] == variable_path:
                    if len(variable_path) < action_path_length:
                        node = self.node_map[variable_path].node
                        if getattr(node, 'action_substitute', None) is not None:
                            action_path_length = len(variable_path)
                            action = node.action_substitute
                    results[variable_path].append(action)
        var_list, words = list(results.values()), [v[1] for v in full_path_engine_variables]
        return var_list, words

class RuleNodeWrapper:

    def __init__(self, node, ancestors, node_ids):
        self.node = node
        self.ancestors = ancestors
        self.full_path = tuple([node_ids[n] for n in ancestors] + [node_ids[node]])
        self.path = tuple(self.full_path[1:])