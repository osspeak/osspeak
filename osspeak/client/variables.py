import collections
from sprecgrammars.rules import astree

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