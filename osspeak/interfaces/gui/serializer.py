import json
from client import cmwatcher, commands
from sprecgrammars.functions.astree import FunctionDefinition
from sprecgrammars.formats.rules.astree import Rule, VariableNode
from sprecgrammars.actions.nodes import RootAction
from client import commands

class GuiEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, commands.CommandModule):
            return obj.config
            # return {
            #     'path': obj.path,
            #     'title': obj.path,
            #     'functions': obj.functions,
            #     'commands': obj.commands,
            #     'variables': obj.variables,
            # }
        if isinstance(obj, FunctionDefinition):
            return {'signature': obj.raw_text, 'action': obj.action.raw_text}
        if isinstance(obj, commands.Command):
            return {'action': obj.action, 'rule': obj.rule}
        if isinstance(obj, RootAction):
            return {'text': obj.raw_text}
        if isinstance(obj, Rule):
            return {'text': obj.raw_text}
        if isinstance(obj, VariableNode):
            return {'name': obj.name, 'rule_text': obj.rule_text}
        return super().default(obj)