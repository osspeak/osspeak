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
        for grouping in parser.groupings + parser.grouping_stack[1:]:
            self.grouping_variables[grouping.id] = grouping
        print(self.grouping_variables)

    def init_action(self, action_text):
        self.action_text = action_text
        parser = ActionParser(self.action_text)
        self.action = parser.parse()

    def perform_action(self, engine_result):
        vars = self.grouping_variables.copy()
        for varid, varval in engine_result['Variables'].items():
            assert varid in vars
            vars[varid] = varval
        print(vars)
        self.action.perform()

    @property
    def id(self):
        return self.rule.id