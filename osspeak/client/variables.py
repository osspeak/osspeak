import collections
from sprecgrammars.rules import astree
from sprecgrammars.actions import nodes
from sprecgrammars.actions.action import Action

class RecognitionResultsTree:

    def __init__(self, root_rule_node, node_ids):
        self.root_rule_node = root_rule_node
        self.node_ids = node_ids
        self.initialize_fields()

    def walk_tree(self):
        for node_info in self.root_rule_node.walk():
            yield RuleNodeWrapper(node_info['node'], node_info['ancestors'], self.node_ids)

    def initialize_fields(self):
        self.node_map = {}
        self.variables = []
        for node_wrapper in self.walk_tree():
            is_ambiguous = (isinstance(node_wrapper.node, astree.GroupingNode) or
                isinstance(node_wrapper.node, astree.Rule) and node_wrapper.node.name == '_dictate')
            if is_ambiguous:
                self.variables.append(node_wrapper.path)
            self.node_map[node_wrapper.path] = node_wrapper

    def get_full_path_engine_variables(self, engine_variables):
        full_path_engine_variables = collections.defaultdict(list)
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
                val = engine_variables[i - 1][1]
                action = self.leaf_action(self.node_map[path].node, val)
                full_path_engine_variables[path].append(action)
                next_path = self.next_path(list(path), var_id)
            path = next_path
        if path:
            val = engine_variables[-1][1]
            action = self.leaf_action(self.node_map[path].node, val)
            full_path_engine_variables[path].append(action)
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
        if isinstance(node, astree.Rule) and node.name == '_dictate':
            return Action(f"'{result_text}'")

    def action_variables(self, engine_variables):
        results = collections.OrderedDict({path: [] for path in self.variables})
        full_path_engine_variables = self.get_full_path_engine_variables(engine_variables)
        for full_path, actions in full_path_engine_variables.items():
            for variable_path in self.variables:
                if full_path[:len(variable_path)] == variable_path:
                    results[variable_path].extend(actions)
        return list(results.values())

class RuleNodeWrapper:

    def __init__(self, node, ancestors, node_ids):
        self.node = node
        self.ancestors = ancestors
        self.full_path = tuple([node_ids[n] for n in ancestors] + [node_ids[node]])
        self.path = tuple(self.full_path[1:])