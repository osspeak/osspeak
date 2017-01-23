import collections
from sprecgrammars.rules import astree
from sprecgrammars.actions import nodes

TreeNodeWrapper = collections.namedtuple('TreeNodeWrapper', ['path', 'node', 'rule_path', 'descendant_ids'])

class RecognitionResultsTree:

    def __init__(self, engine_variables, root_rule_node):
        self.root_rule_node = root_rule_node
        self.engine_variables = engine_variables
        self.init_everything()

    def init_everything(self):
        self.rule_paths = {}
        # {'ruleid': {'child id': 'child full path'}}
        self.rule_children = collections.defaultdict(dict)
        self.groupings = collections.OrderedDict()
        self.tree_node_map = {}
        for node_wrapper in self.tree_nodes():
            self.tree_node_map[node_wrapper.path] = node_wrapper
            assert isinstance(node_wrapper.rule_path, tuple)
            if isinstance(node_wrapper.node, astree.Rule):
                self.rule_paths[node_wrapper.node.id] = node_wrapper
            if isinstance(node_wrapper.node, astree.GroupingNode):
                self.groupings[node_wrapper.path] = node_wrapper                
            self.rule_children[node_wrapper.rule_path][node_wrapper.path[-1]] = node_wrapper.path
        for k in self.rule_children:
            assert isinstance(k, tuple)

    def magic(self):
        current_node = None
        magic_list = []
        current_rule_wrapper = self.rule_paths[self.root_rule_node.id]
        for i, (var_id, var_val) in enumerate(self.engine_variables):
            # rely on all rule ids to be unique
            if var_id in self.rule_paths:
                current_rule_wrapper = self.rule_paths[var_id]
                magic_list.append([current_rule_wrapper.path, ''])
                continue
            # go up until we find containing rule
            while var_id not in current_rule_wrapper.descendant_ids:
                assert current_rule_wrapper.node is not self.root_rule_node
                current_rule_wrapper = self.rule_paths[current_rule_wrapper.path[:-1]]
            full_path = self.rule_children[current_rule_wrapper.path][var_id]
            magic_list.append([full_path, var_val])
        return magic_list

    def leaf_action(self, node):
        if getattr(node, 'action_substitute', None) is not None:
            return node.action_substitute
        if isinstance(node, astree.WordNode):
           return nodes.LiteralKeysAction(node.text)

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

    @property
    def action_variables(self):
        results = collections.defaultdict(list)
        full_path_engine_variables = self.magic()
        for i, (full_path, var_text) in enumerate(full_path_engine_variables):
            node_wrapper = self.tree_node_map[full_path]
            action = self.leaf_action(node_wrapper.node)
            if action is not None:
                for j, node_id in enumerate(full_path, start=1):
                    # 'abcd' => 'a' 'ab', 'abc', 'abcd'
                    partial_path = full_path[:j]
                    results[partial_path].append(action)
        variables = []
        for grouping_path in self.groupings:
            action = nodes.RootAction()
            action.children = results.get(grouping_path, [])
            variables.append(action)
        return variables
