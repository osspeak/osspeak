import json
import os
from settings import settings
from recognition.commands import monitor

async def delete_command_module(path):
    try:
        os.remove(path)
    except OSError:
        pass

async def recognition_index(grammar_id=None):
    command_modules = monitor.command_module_state.command_modules
    root = settings['command_directory']
    command_modules = {}
    for path, command_module in monitor.command_module_state.command_modules.items():
        relpath = os.path.relpath(path, root)
        command_modules[relpath] = command_module_object(command_module)
    return {
        'commandModules': command_modules,
        'osSep': os.sep
    }
    
def command_module_object(command_module):
    commands = []
    for cmd in command_module.commands:
        rule = {'text': cmd.rule.text}
        action = {'pieces': []}
        for piece in cmd.action.pieces:
            action['pieces'].append({
                'type': piece.json_object['type'],
                'value': piece.json_object['value']
            })
        commands.append({'rule': rule, 'action': action})
    return {
        'commands': commands
    }