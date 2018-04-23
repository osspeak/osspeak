import os
from settings import settings
from recognition.commands import monitor

def command_modules():
    state_json = monitor.command_module_state.command_module_json
    root = settings['command_directory']
    module_paths = []
    for path, config in state_json.items():
        relpath = os.path.relpath(path, root)
        split_path = relpath.split(os.sep)[:]
        module_paths.append(split_path)
    return {
        'paths': module_paths
    }

def command_module(path):
    full_path = os.path.join(settings['command_directory'], *path)
    module = monitor.command_module_state.command_modules[full_path]
    commands = []
    for cmd in module.commands:
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
    print(dir(module))
    return 'banan'