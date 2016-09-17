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
        self.init_rule()
        self.init_action()

    def init_rule(rule_text):
        self.rule_text = rule_text
        parser = VocolaParser(cmd)
        self.rule = parser.parse_as_rule()

    def init_action(action_text):
        self.action_text = action_text
        parser = ActionParser(self.action_text)
        self.action = parser.parse()

    def id(self):
        return self.rule.id