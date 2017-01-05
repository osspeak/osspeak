import collections
import itertools
import json

from sprecgrammars.actions.parser import ActionParser
from sprecgrammars.actions import nodes
from sprecgrammars.functions.parser import FunctionDefinitionParser
from sprecgrammars import api
from interfaces.gui import serializer
from client import commands, scopes
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

    @property
    def conditions(self):
        return self.config.get('conditions', {})

    def to_dict(self):
        jsonstr = json.dumps(self, cls=serializer.GuiEncoder)
        return json.loads(jsonstr) 

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
        bound_variables = collections.OrderedDict()
        engine_variables = {var[0]: var[1] for var in engine_result['Variables'] if len(var) == 2}
        for rule_node in self.rule.children:
            self.add_var_action(rule_node, engine_variables, bound_variables)
        var_list = list(bound_variables.values())
        self.action.perform(var_list)
        
    def add_var_action(self, rule_node, engine_variables, bound_variables):
        if not isinstance(rule_node, (astree.Rule, astree.GroupingNode)):
            return
        matched_children = self.get_matched_children(rule_node, engine_variables)
        if not matched_children:
            return
        action = nodes.RootAction()
        for child in matched_children:
            if getattr(child, 'action_substitute', None):
                action.children.append(child.action_substitute)
            elif isinstance(child, astree.WordNode):
                action.children.append(nodes.LiteralKeysAction(child.text))
            elif isinstance(child, (astree.Rule, astree.GroupingNode)):
                child_action = self.add_var_action(child, engine_variables, bound_variables)
                action.children.append(child_action)
        if isinstance(rule_node, astree.GroupingNode):
            bound_variables[rule_node.id] = action
        return action

    def get_matched_children(self, parent_node, engine_variables):
        matched_children = []
        is_match = False
        for child in parent_node.children:
            if isinstance(child, astree.OrNode):
                if is_match:
                    break
                matched_children = []
            if child.id in engine_variables:
                is_match = True
            matched_children.append(child)
        return matched_children
            