import json
from client import cmwatcher, commands
from sprecgrammars.functions.astree import FunctionDefinition
from sprecgrammars.rules.astree import Rule
from sprecgrammars.actions.nodes import RootAction
from client import commands

class GuiEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, commands.CommandModule):
            return obj.config
        if isinstance(obj, FunctionDefinition):
            return {'signature': obj.raw_text, 'action': obj.action.raw_text}
        if isinstance(obj, commands.Command):
            return {'action': obj.action, 'rule': obj.rule}
        if isinstance(obj, RootAction):
            return {'text': obj.raw_text}
        if isinstance(obj, Rule):
            return {'text': obj.raw_text}
        return super().default(obj)