import collections

from sprecgrammars.actions.parser import ActionParser
from client import commands
from sprecgrammars import astree
from sprecgrammars.formats import VocolaParser, SrgsXmlConverter

class CommandModule:

    def __init__(self, config):
        self.config = config
        self.commands = []

    def load_commands(self):
        for rule_text, action_text in self.config['Commands']:
            cmd = Command(rule_text, action_text)
            self.commands.append(cmd)

class Command:
    
    def __init__(self, rule_text, action_text):
        self.init_rule(rule_text)
        self.init_action(action_text)

    def init_rule(self, rule_text):
        self.rule_text = rule_text
        parser = VocolaParser(self.rule_text)
        self.rule = parser.parse_as_rule()
        self.grouping_variables = collections.OrderedDict()
        # make a copy in perform_action to keep track of string values
        self.grouping_variables_values = collections.OrderedDict()
        for grouping in parser.groupings + parser.grouping_stack[1:]:
            self.grouping_variables[grouping.id] = grouping
            self.grouping_variables_values[grouping.id] = ''
        print(self.grouping_variables)

    def init_action(self, action_text):
        self.action_text = action_text
        parser = ActionParser(self.action_text)
        self.action = parser.parse()

    def perform_action(self, engine_result):
        grouping_vars = self.grouping_variables_values.copy()
        for varid, varval in engine_result['Variables'].items():
            assert varid in grouping_vars
            grouping_vars[varid] = varval
        self.assign_parent_variables(engine_result['Variables'], grouping_vars)
        var_list = list(grouping_vars.values())
        print(var_list)
        self.action.perform()

    def assign_parent_variables(self, result_vars, grouping_vars):
        for ruleid in result_vars:
            if result_vars[ruleid]:
                continue
            print('rid ', ruleid)
            self.assign_variable(self.grouping_variables[ruleid], grouping_vars)

    def assign_variable(self, grouping, grouping_vars):
        val_list = []
        correct_option = False
        print(grouping_vars)
        if grouping_vars[grouping.id]:
            return grouping_vars[grouping.id]
        for child in grouping.children:
            if isinstance(child, astree.WordNode):
                val_list.append(child.text)
                print(child.text)
            print(child)
        grouping_vars[grouping.id] = ' '.join(val_list)

    @property
    def id(self):
        return self.rule.id