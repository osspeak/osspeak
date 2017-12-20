import json
from client import commands
from recognition.rules.astree import Rule
from client import commands

class GuiEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, commands.CommandModule):
            return {
                'rules': obj.rules,
                'functions': obj.functions,
                'commands': obj.commands,
                'path': obj.path,
                'scope': getattr(obj.scope, 'name', None),
                'conditions': obj.conditions,
                'error': None,
            }
        if isinstance(obj, FunctionDefinition):
            return {'signature': {'value': obj.raw_text, 'errors': []}, 'action': obj.action}
        if isinstance(obj, commands.Command):
            return {'rule': obj.rule, 'action': obj.action}
        if isinstance(obj, RootAction):
            return {'value': obj.raw_text, 'errors': []}
        if isinstance(obj, Rule):
            return {'name': {'value': obj.name, 'errors': []}, 'value': {'value': obj.raw_text, 'errors': []}}
        return super().default(obj)