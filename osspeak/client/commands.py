import collections
import itertools
import json

from sprecgrammars.actions.parser import ActionParser
from sprecgrammars.actions import nodes
from sprecgrammars.functions.parser import FunctionDefinitionParser
from sprecgrammars import api
from interfaces.gui import serializer
from client import commands, scopes, variables
from sprecgrammars.rules import astree
from sprecgrammars.rules.parser import RuleParser

class CommandModule:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.scope = None
        self.rules = []
        self.functions = []
        self.commands = []
        # currently activate and deactivate
        self.events = {}

    def load_commands(self):
        for rule_text, action_text in self.config.get('commands', {}):
            cmd = Command(rule_text, action_text, scope=self.scope)
            self.commands.append(cmd)

    def initialize_rules(self):
        for rule_name, rule_text in self.config.get('rules', {}):
            self.scope._rules[rule_name] = rule_text

    def load_rules(self):
        for rule_name, rule_text in self.config.get('rules', {}):
            current_rule = self.scope._rules[rule_name]
            if isinstance(current_rule, astree.Rule):
                assert current_rule.name is not None
                self.rules.append(current_rule)
                continue
            assert isinstance(current_rule, str)
            self.scope._rules[rule_name] = None
            rule = api.rule(rule_text, name=rule_name, rules=self.scope._rules)
            self.scope._rules[rule_name] = rule
            self.rules.append(rule)

    def define_functions(self):
        for func_signature, func_text in self.config.get('functions', {}):
            func_definition = api.func_definition(func_signature, defined_functions=self.scope.functions)
            self.scope._functions[func_definition.name] = func_definition
            self.functions.append(func_definition)

    def set_function_actions(self):
        config_funcs = self.config.get('functions', {})
        for i, func in enumerate(self.functions):
            action_text = config_funcs[i][1]
            func.action = api.action(action_text, defined_functions=self.scope.functions)

    def load_events(self):
        for event_name, event_text in self.config.get('events', {}).items():
            self.events[event_name] = api.action(event_text, defined_functions=self.scope.functions)

    @property
    def conditions(self):
        return self.config.get('conditions', {})

class Command:
    
    def __init__(self, rule_text, action_text, scope=None):
        self.scope = scopes.Scope() if scope is None else scope
        self.init_rule(rule_text)
        self.init_action(action_text)

    def init_rule(self, rule_text):
        self.rule_text = rule_text
        self.rule = api.rule(rule_text, rules=self.scope.rules)

    def init_action(self, action_text):
        self.action_text = action_text
        self.action = api.action(action_text, self.scope.functions)

    @property
    def id(self):
        return self.rule.id

    def perform_action(self, engine_result):
        # empty variables dict, gets filled based on result
        # bound_variables = variables.build_grouping_map(self.rule)
        engine_variables = tuple(v for v in engine_result['Variables'] if len(v) == 2)
        variable_tree = variables.RecognitionResultsTree(engine_variables, self.rule)
        var_list = variable_tree.action_variables
        print('asdasda', var_list, end=' ')
        # for rule_node in self.rule.children:
        #     self.add_var_action(rule_node, engine_variables, bound_variables, [self.rule.id])
        # var_list = [nodes.RootAction() if a is None else a for a in bound_variables.values()]
        self.action.perform(var_list)
        
    def add_var_action(self, rule_node, engine_variables, bound_variables, ancestor_ids):
        if not isinstance(rule_node, (astree.Rule, astree.GroupingNode)):
            return
        ancestor_ids = [rule_node.id] if ancestor_ids is None else ancestor_ids + [rule_node.id]
        action = nodes.RootAction()
        rule_dictation = self.get_rule_dictation(rule_node, engine_variables)
        if rule_dictation is not None:
            action.children.append(nodes.LiteralKeysAction(rule_dictation))
            bound_variables[rule_node.id] = action
            return action
        matched_children = self.get_matched_children(rule_node, engine_variables)
        for child in matched_children:
            if getattr(child, 'action_substitute', None):
                action.children.append(child.action_substitute)
            elif isinstance(child, astree.WordNode):
                action.children.append(nodes.LiteralKeysAction(child.text))
            elif isinstance(child, (astree.Rule, astree.GroupingNode)):
                child_action = self.add_var_action(child, engine_variables, bound_variables, ancestor_ids)
                action.children.append(child_action)
        if isinstance(rule_node, astree.GroupingNode):
            node_path = tuple(ancestor_ids)
            assert bound_variables.get(node_path, False) is None
            bound_variables[node_path] = action
        return action

    def get_matched_children(self, parent_node, engine_variables):
        # inefficient, but probably doesn't matter
        if not parent_node.children:
            return []
        matched_children = []
        child_id_map = {c.id: c for c in parent_node.children}
        descendant_ids = set(variables.get_descendant_ids(parent_node))
        for var_id, var_text in engine_variables:
            if matched_children and var_id not in descendant_ids:
                break
            if var_id in child_id_map:
                matched_children.append(child_id_map[var_id])
        return matched_children

    def get_rule_dictation(self, rule_node, engine_variables):
        if not isinstance(rule_node, (astree.Rule)) or rule_node.name != '_dictate':
            return
        match_id = f'dictation-{rule_node.id}'
        for var_id, var_text in engine_variables:
            if var_id == match_id:
                return var_text