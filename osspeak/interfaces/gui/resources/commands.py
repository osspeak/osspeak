import json
import os
from settings import settings
from recognition.commands import monitor

async def command_module_paths():
    state_json = {path: mod.config for path, mod in monitor.command_module_state.command_modules.items()}
    root = settings['command_directory']
    module_paths = []
    for path, config in state_json.items():
        relpath = os.path.relpath(path, root)
        module_paths.append(relpath)
    return {
        'paths': module_paths,
        'osSep': os.sep
    }
async def recognition_index():
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