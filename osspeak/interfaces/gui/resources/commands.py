import json
import os
from settings import settings
from communication import topics, pubsub
import copy
from recognition.commands import monitor

async def delete_command_module(path):
    try:
        os.remove(path)
    except OSError:
        pass

async def save_command(command, index, command_module_path):
    print('save', command, index)
    state = monitor.command_module_state
    full_path = os.path.join(settings['command_directory'], command_module_path)
    command_module = state.command_modules[full_path]
    config = copy.copy(command_module.config)
    config['commands'] = copy.copy(config.get('commands', []))
    config['commands'][index] = translated_client_command(command)
    with open(full_path, 'w') as f:
        json.dump(config, f, indent=4, sort_keys=True)
    pubsub.publish(topics.RELOAD_COMMAND_MODULE_FILES)

def translated_client_command(client_command):
    rule = client_command['rule']['text']
    pieces = client_command['action']['pieces']
    if len(pieces) == 1:
        action = pieces[0]['value']
    else:
        action = pieces
    return [rule, action]
    # rule, action = client_command

def save_module_changes(to_update, to_delete):
    print(to_update)
    root = settings['command_directory']
    state = monitor.command_module_state
    for command_module in to_update:
        full_path = os.path.join(root, command_module['path'])
        try:
            existing_config = state.command_modules[full_path].config
        except KeyError:
            existing_config = {}
        updated_config = {**existing_config, **command_module['config']}
        with open(full_path, 'w') as f:
            json.dump(updated_config, f)
    return 4

async def recognition_index(grammar_id=None):
    root = settings['command_directory']
    state = monitor.command_module_state
    command_modules = {}
    for path, command_module in state.command_modules.items():
        relpath = os.path.relpath(path, root)
        command_modules[relpath] = command_module_object(command_module)
    active_command_modules = [os.path.relpath(name, root) for name in state.active_command_modules]
    return {
        'commandModules': command_modules,
        'activeCommandModules': active_command_modules,
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