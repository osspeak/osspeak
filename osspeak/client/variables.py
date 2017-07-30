import collections
from sprecgrammars.rules import astree
from sprecgrammars.actions import nodes

TreeNodeWrapper = collections.namedtuple('TreeNodeWrapper', ['path', 'node', 'rule_path', 'descendant_ids'])

class RecognitionResultsTree:

    def __init__(self, root_rule_node, node_ids):
        self.root_rule_node = root_rule_node
        self.node_ids = node_ids
        self.initialize_fields()

    def walk_tree(self):
        for node_info in self.root_rule_node.walk():
            yield RuleNodeWrapper(node_info['node'], node_info['ancestors'], self.node_ids)

    def initialize_fields(self):
        self.rule_paths = {}
        # {'ruleid': {'child id': 'child full path'}}
        self.rule_children = collections.defaultdict(dict)
        self.ambiguities = collections.OrderedDict()
        self.tree_node_map = {}
        self.node_map = {}
        self.variables = collections.OrderedDict()
        self.tree = list(self.walk_tree())
        for node_wrapper in self.tree:
            is_ambiguous = (isinstance(node_wrapper.node, astree.GroupingNode) or
                isinstance(node_wrapper.node, astree.Rule) and node_wrapper.node.name == '_dictate')
            if is_ambiguous:
                self.variables[node_wrapper.path] = node_wrapper
            self.node_map[node_wrapper.path] = node_wrapper
        for node_wrapper in self.tree_nodes():
            self.tree_node_map[node_wrapper.path] = node_wrapper
            assert isinstance(node_wrapper.rule_path, tuple)
            if isinstance(node_wrapper.node, astree.Rule):
                node_id = self.node_ids[node_wrapper.node]
                self.rule_paths[node_id] = node_wrapper
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
        current_rule_wrapper = self.rule_paths[self.node_ids[self.root_rule_node]]
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
            full_rule_path = current_rule_wrapper.rule_path + (self.node_ids[current_rule_wrapper.node],)
            full_path = self.rule_children[full_rule_path][var_id]
            full_path_engine_variables.append([full_path, var_val])
        return full_path_engine_variables

    def get_full_path_engine_variables2(self, engine_variables):
        full_path_engine_variables = collections.defaultdict(list)
        path = ()
        for i, (var_id, var_val) in enumerate(engine_variables):
            if path not in self.node_map:
                path = ()
                continue
            next_path = path + (var_id,)
            if next_path not in self.node_map:
                val = engine_variables[i - 1][1]
                action = self.leaf_action(self.node_map[path].node, ' '.join(val))
                full_path_engine_variables[path].append(action)
                next_path = self.next_path(list(path), var_id)
            path = next_path
        if path:
            val = engine_variables[-1][1]
            action = self.leaf_action(self.node_map[path].node, ' '.join(val))
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
           return nodes.LiteralKeysAction(node.text)
        if isinstance(node, astree.Rule) and node.name == '_dictate':
           return nodes.LiteralKeysAction(result_text)

    def tree_nodes(self, root=None, root_path=None, rule_path=None):
        root = self.root_rule_node if root is None else root
        rule_path = [] if rule_path is None else rule_path
        root_id = self.node_ids[root]
        path = [root_id] if root_path is None else root_path + [root_id]
        for child in getattr(root, 'children', []):
            child_rule_path = rule_path + [root_id] if isinstance(root, astree.Rule) else rule_path 
            yield from self.tree_nodes(child, path, child_rule_path)
        descendant_ids = set(self.get_descendant_ids(root))
        yield TreeNodeWrapper(tuple(path), root, tuple(rule_path), descendant_ids)

    def get_descendant_ids(self, node):
        descendant_ids = []
        for child in getattr(node, 'children', []):
            descendant_ids.extend(self.get_descendant_ids(child) + [self.node_ids[child]])
        return descendant_ids

    def action_variables(self, engine_variables):
        results = collections.OrderedDict({path: nodes.RootAction() for path in self.variables})
        full_path_engine_variables = self.get_full_path_engine_variables2(engine_variables)
        for i, (full_path, actions) in enumerate(full_path_engine_variables.items()):
            for grouping_path, node_wrapper in self.variables.items():
                if full_path[:len(grouping_path)] == grouping_path:
                    results[grouping_path].children.extend(actions)
        return list(results.values())

class RuleNodeWrapper:

    def __init__(self, node, ancestors, node_ids):
        self.node = node
        self.descendant_ids = self.get_descendant_ids(node_ids)
        self.ancestors = ancestors
        self.full_path = tuple([node_ids[n] for n in ancestors] + [node_ids[node]])

    def get_descendant_ids(self, node_ids):
        descendants = list(info['node'] for info in self.node.walk())[1:]
        return set(node_ids[n] for n in descendants)

    @property
    def path(self):
        return tuple(self.full_path[1:])