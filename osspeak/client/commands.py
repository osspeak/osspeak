import collections

from sprecgrammars.actions.parser import ActionParser
from client import commands
from sprecgrammars.formats.rules import astree
from sprecgrammars.formats import RuleParser, SrgsXmlConverter

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
        parser = RuleParser(self.rule_text)
        self.rule = parser.parse_as_rule()
        self.grouping_variables = collections.OrderedDict()
        # make a copy in perform_action to keep track of string values
        self.grouping_variables_values = collections.OrderedDict()
        for grouping in parser.groupings + parser.grouping_stack[1:]:
            self.grouping_variables[grouping.id] = grouping
            self.grouping_variables_values[grouping.id] = ''

    def init_action(self, action_text):
        self.action_text = action_text
        parser = ActionParser(self.action_text)
        self.action = parser.parse()

    def perform_action(self, engine_result):
        grouping_vars = self.grouping_variables_values.copy()
        print(self.grouping_variables)
        for varid, varval in engine_result['Variables'].items():
            assert varid in grouping_vars
            grouping_vars[varid] = varval
        self.assign_parent_variables(engine_result['Variables'], grouping_vars)
        var_list = list(grouping_vars.values())
        self.action.perform()

    def assign_parent_variables(self, result_vars, grouping_vars):
        for ruleid in result_vars:
            if result_vars[ruleid]:
                continue
            self.assign_variable(self.grouping_variables[ruleid], result_vars, grouping_vars)

    def assign_variable(self, grouping, result_vars, grouping_vars):
        '''
        Traverse the grouping tree to assign a text value to all matched
        groupings. This implementation rests on the
        assumption that only leaf groupings have matching text information.
        Groupings that don't match any words and don't
        have any matching children do not get transmitted by the engine.
        '''
        val_list = []
        correct_option = False
        if grouping_vars[grouping.id]:
            return grouping_vars[grouping.id]
        for child in grouping.children:
            if isinstance(child, astree.WordNode):
                val_list.append(child.text)
            elif isinstance(child, astree.GroupingNode):
                if child.id in result_vars:
                    correct_option = True
                    self.assign_variable(child, result_vars, grouping_vars)
                    val_list.append(grouping_vars[child.id])
                else:
                    assert not correct_option
            elif isinstance(child, astree.OrNode):
                if correct_option:
                    break
                val_list = []
        grouping_vars[grouping.id] = ' '.join(val_list)

    @property
    def id(self):
        return self.rule.id