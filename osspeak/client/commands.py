import collections

from sprecgrammars.actions.parser import ActionParser
from sprecgrammars.actions import nodes
from client import commands
from sprecgrammars.formats.rules import astree
from sprecgrammars.formats import RuleParser, SrgsXmlConverter

class CommandModule:

    def __init__(self, config):
        self.config = config
        self.commands = []
        self.variables = []

    def load_commands(self, varmap):
        for rule_text, action_text in self.config['Commands']:
            cmd = Command(rule_text, action_text, variables=varmap)
            self.commands.append(cmd)

    def load_variables(self, varmap):
        for varname, rule_text in self.config['Variables']:
            var = astree.VariableNode(varname, rule_text, varmap)
            varmap[varname] = var
            self.variables.append(var)

class Command:
    
    def __init__(self, rule_text, action_text, variables=None):
        self.variables = variables
        self.init_rule(rule_text)
        self.init_action(action_text)

    def init_rule(self, rule_text):
        self.rule_text = rule_text
        parser = RuleParser(self.rule_text, self.variables)
        self.rule = parser.parse_as_rule()

    def init_action(self, action_text):
        self.action_text = action_text
        parser = ActionParser(self.action_text)
        self.action = parser.parse()

    def perform_action(self, engine_result):
        # empty variables dict, gets filled based on result
        grouping_vars = self.rule.grouping_variables.copy()
        for k in grouping_vars:
            grouping_vars[k] = None
        print(grouping_vars)
        for varid, varval in engine_result['Variables'].items():
            assert varid in grouping_vars
            grouping_vars[varid] = varval
        substitution_ids = set(engine_result['SubstitutionIds'])
        self.assign_parent_variables(engine_result['Variables'], grouping_vars, substitution_ids)
        var_list = list(grouping_vars.values())
        print(var_list[0].children[0].children[0])
        self.action.perform(var_list)

    def assign_parent_variables(self, result_vars, grouping_vars, substitution_ids):
        for ruleid in result_vars:
            if result_vars[ruleid]:
                continue
            self.assign_variable(self.rule.grouping_variables[ruleid], result_vars, grouping_vars, substitution_ids)

    def assign_variable(self, grouping, result_vars, grouping_vars, substitution_ids):
        '''
        Traverse the grouping tree to assign a text value to all matched
        groupings. This implementation rests on the
        assumption that only leaf groupings have matching text information.
        Groupings that don't match any words and don't
        have any matching children do not get transmitted by the engine.
        '''
        if grouping_vars[grouping.id]:
            return grouping_vars[grouping.id]
        variable_action = nodes.RootAction()
        # grouping is a container of other Rules pieces, meaning only
        # one child can match for each recognition
        correct_option = False
        for child in grouping.children:
            if isinstance(child, astree.WordNode):
                if child.id in substitution_ids:
                    action = child.action_substitute
                    correct_option = True
                else:
                    action = nodes.LiteralKeysAction(child.text)
                variable_action.children.append(action)
            elif isinstance(child, astree.GroupingNode):
                if child.id in result_vars:
                    correct_option = True
                    self.assign_variable(child, result_vars, grouping_vars, substitution_ids)
                    variable_action.children.append(grouping_vars[child.id])
                else:
                    assert not correct_option
            elif isinstance(child, astree.OrNode):
                if correct_option:
                    break
                variable_action.children = []
        grouping_vars[grouping.id] = variable_action

    @property
    def id(self):
        return self.rule.id