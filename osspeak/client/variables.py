import collections
from sprecgrammars.rules import astree
from sprecgrammars.actions import nodes

TreeNodeWrapper = collections.namedtuple('TreeNodeWrapper', ['path', 'node', 'rule_path', 'descendant_ids'])

class RecognitionResultsTree:

    def __init__(self, root_rule_node):
        self.root_rule_node = root_rule_node
        self.init_everything()

    def init_everything(self):
        self.rule_paths = {}
        # {'ruleid': {'child id': 'child full path'}}
        self.rule_children = collections.defaultdict(dict)
        self.ambiguities = collections.OrderedDict()
        self.tree_node_map = {}
        for node_wrapper in self.tree_nodes():
            self.tree_node_map[node_wrapper.path] = node_wrapper
            assert isinstance(node_wrapper.rule_path, tuple)
            if isinstance(node_wrapper.node, astree.Rule):
                self.rule_paths[node_wrapper.node.id] = node_wrapper
            is_ambiguous = (isinstance(node_wrapper.node, astree.GroupingNode) or
                            isinstance(node_wrapper.node, astree.Rule) and node_wrapper.node.name == '_dictate')
            if is_ambiguous:
                self.ambiguities[node_wrapper.path] = node_wrapper
            self.rule_children[node_wrapper.rule_path][node_wrapper.path[-1]] = node_wrapper.path
        for k in self.rule_children:
            assert isinstance(k, tuple)

    def get_full_path_engine_variables(self, engine_variables):
        current_node = None
        full_path_engine_variables = []
        current_rule_wrapper = self.rule_paths[self.root_rule_node.id]
        for i, (var_id, var_val) in enumerate(engine_variables):
            split_id = var_id.split('-')
            if split_id[0] == 'dictation':
                var_id = split_id[1]
            # rely on all rule ids to be unique
            if var_id in self.rule_paths:
                current_rule_wrapper = self.rule_paths[var_id]
                full_path_engine_variables.append([current_rule_wrapper.path, var_val])
                continue
            # go up until we find containing rule
            while var_id not in current_rule_wrapper.descendant_ids:
                assert current_rule_wrapper.node is not self.root_rule_node
                current_rule_wrapper = self.rule_paths[current_rule_wrapper.rule_path[-1]]
            full_rule_path = current_rule_wrapper.rule_path + (current_rule_wrapper.node.id,)
            full_path = self.rule_children[full_rule_path][var_id]
            full_path_engine_variables.append([full_path, var_val])
        return full_path_engine_variables

    def leaf_action(self, node, result_text):
        if getattr(node, 'action_substitute', None) is not None:
            return node.action_substitute
        if isinstance(node, astree.WordNode):
           return nodes.LiteralKeysAction(node.text)
        if isinstance(node, astree.Rule) and node.name == '_dictate':
           return nodes.LiteralKeysAction(result_text)

    def tree_nodes(self, root=None, root_path=None, rule_path=None):
        root = self.root_rule_node if root is None else root
        rule_path = [] if rule_path is None else rule_path
        path = [root.id] if root_path is None else root_path + [root.id]
        for child in getattr(root, 'children', []):
            child_rule_path = rule_path + [root.id] if isinstance(root, astree.Rule) else rule_path 
            yield from self.tree_nodes(child, path, child_rule_path)
        descendant_ids = set(self.get_descendant_ids(root))
        yield TreeNodeWrapper(tuple(path), root, tuple(rule_path), descendant_ids)

    def get_descendant_ids(self, node):
        descendant_ids = []
        for child in getattr(node, 'children', []):
            descendant_ids.extend(self.get_descendant_ids(child) + [child.id])
        return descendant_ids

    def action_variables(self, engine_variables):
        results = collections.defaultdict(list)
        full_path_engine_variables = self.get_full_path_engine_variables(engine_variables)
        for i, (full_path, var_text) in enumerate(full_path_engine_variables):
            node_wrapper = self.tree_node_map[full_path]
            action = self.leaf_action(node_wrapper.node, var_text)
            if action is not None:
                for j, node_id in enumerate(full_path, start=1):
                    # 'abcd' => 'a' 'ab', 'abc', 'abcd'
                    partial_path = full_path[:j]
                    results[partial_path].append(action)
        variables = []
        for grouping_path in self.ambiguities:
            action = nodes.RootAction()
            action.children = results.get(grouping_path, [])
            variables.append(action)
        return variables
