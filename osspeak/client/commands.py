import collections
import itertools

from sprecgrammars.actions.parser import ActionParser
from sprecgrammars.actions import nodes
from sprecgrammars.functions.parser import FunctionDefinitionParser
from sprecgrammars import api
from client import commands, scopes
from sprecgrammars.formats.rules import astree
from sprecgrammars.formats import RuleParser, SrgsXmlConverter

class CommandModule:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.scope = None
        self.functions = []
        self.commands = []
        self.variables = []

    def load_commands(self):
        for rule_text, action_text in self.config.get('Commands', {}):
            cmd = Command(rule_text, action_text, scope=self.scope)
            self.commands.append(cmd)

    def load_variables(self):
        for varname, rule_text in self.config.get('Variables', {}):
            var = api.variable(varname, rule_text, self.scope.variables)
            self.scope._variables[varname] = var
            self.variables.append(var)

    def load_functions(self):
        for func_signature, func_text in self.config.get('Functions', {}):
            func_definition = api.func_definition(func_signature, func_text, defined_functions=self.scope.functions)
            self.scope._functions[func_definition.name] = func_definition
            self.functions.append(func_definition)

class Command:
    
    def __init__(self, rule_text, action_text, scope=None):
        self.scope = scopes.Scope() if scope is None else scope
        self.init_rule(rule_text)
        self.init_action(action_text)

    def init_rule(self, rule_text):
        self.rule_text = rule_text
        self.rule = api.rule(rule_text, self.scope.variables)

    def init_action(self, action_text):
        self.action_text = action_text
        self.action = api.action(action_text, self.scope.functions)

    def perform_action(self, engine_result):
        # empty variables dict, gets filled based on result
        bound_variables = self.rule.grouping_variables_empty.copy()
        idx = 0
        while idx < len(engine_result['Variables']):
            increment = self.bind_variable(bound_variables, engine_result['Variables'], idx)
            idx += increment
        var_list = list(bound_variables.values())
        self.action.perform(var_list)

    def bind_variable(self, bound_variables, semantic_variables, idx):
        var_id, var_text = semantic_variables[idx]
        increment = 1
        grouping_node = self.rule.grouping_variables.get(var_id)
        if grouping_node is None:
            return increment
        if bound_variables[var_id] is None:
            bound_variables[var_id] = nodes.RootAction()
        increment += self.bind_child_variables(idx, var_id, bound_variables, semantic_variables, grouping_node)
        if grouping_node.action_substitute is not None:
            bound_variables[var_id] = grouping_node.action_substitute
        return increment

    def bind_child_variables(self, idx, var_id, bound_variables, semantic_variables, parent_node):
        # parent node stats as grouping node, can become rule node when
        # a variable is encountered
        var_action = bound_variables[var_id]
        idx += 1
        increment = 0
        child_ids = parent_node.child_ids
        while idx < len(semantic_variables):
            remaining_id, remaining_text = semantic_variables[idx]
            if remaining_id == 'literal-{}'.format(var_id):
                var_action.children.append(nodes.LiteralKeysAction(remaining_text))
                idx += 1
                increment += 1
            elif remaining_id in child_ids:
                child_node = child_ids[remaining_id]
                if isinstance(child_node, astree.WordNode):
                    assert remaining_id.startswith('s')
                    var_action.children.append(child_node.action_substitute)
                    idx += 1
                    increment += 1
                    continue
                # assuming we have a child grouping here
                remaining_increment = self.bind_variable(bound_variables, semantic_variables, idx)
                var_action.children.append(bound_variables[remaining_id])
                idx += remaining_increment
                increment += remaining_increment
            else:
                for child in parent_node.children:
                    if isinstance(child, astree.VariableNode):
                        if remaining_id == child.rule.id:
                            parent_node = child.rule
                            child_ids = {c.id: c for c in parent_node.children}
                            idx += 1
                            increment += 1
                            break
                else:
                    break
        return increment

    @property
    def id(self):
        return self.rule.id