import collections
from sprecgrammars.rules import astree
from sprecgrammars.actions import nodes

def get_descendant_ids(rule_node):
    descendant_ids = []
    for child in rule_node.children:
        if isinstance(child, (astree.Rule, astree.GroupingNode)):
            descendant_ids.extend(get_descendant_ids(child))
        descendant_ids.append(child.id)
    return descendant_ids

def build_grouping_map(node, grouping_map=None, ancestor_ids=None):
    grouping_map = collections.OrderedDict() if grouping_map is None else grouping_map
    ancestor_ids = [node.id] if ancestor_ids is None else ancestor_ids + [node.id]
    for child in getattr(node, 'children', []):
        build_grouping_map(child, grouping_map, ancestor_ids)
    if isinstance(node, astree.GroupingNode):
        node_path = tuple(ancestor_ids)
        assert node_path not in grouping_map
        grouping_map[node_path] = None
    return grouping_map

class RecognitionResultsTree:

    def __init__(self, engine_variables, root_rule_node):

        self.engine_variables = engine_variables
        self.root_rule_node = root_rule_node
        self.grouping_ids = [p for p, n in self.tree_nodes() if isinstance(n, astree.GroupingNode)]
        self.engine_variable_set = set(v[0] for v in self.engine_variables)
        self.init_actions()

    @property
    def action_variables(self):
        variables = []
        for _id in self.grouping_ids:
            variable_action = nodes.RootAction()
            variable_action.children = self.actions[_id]
            variables.append(variable_action)
        return variables

    def init_actions(self):
        self.actions = collections.defaultdict(list)
        paths = [(path, node) for (path, node) in self.tree_nodes() if path[-1] in self.engine_variable_set]
        for path, node in paths:
            action = self.leaf_action(node)
            if action is not None:
                # add action to path and all ancestor paths
                for i, ancestor_name in enumerate(path):
                    ancestor_path = path[:i]
                    self.actions[ancestor_path].append(action)
        x=4

    def leaf_action(self, node):
        if getattr(node, 'action_substitute', None) is not None:
            return node.action_substitute
        if isinstance(node, astree.WordNode):
           return nodes.LiteralKeysAction(node.text)

    def tree_nodes(self, root=None, root_path=None):
        root = self.root_rule_node if root is None else root
        path = [root.id] if root_path is None else root_path + [root.id]
        for child in getattr(root, 'children', []):
            yield from self.tree_nodes(child, path)
        yield tuple(path), root