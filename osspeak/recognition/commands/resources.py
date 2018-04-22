import os
from settings import settings
from recognition.commands import monitor

def command_modules():
    state_json = monitor.command_module_state.command_module_json
    root = settings['command_directory']
    module_paths = []
    for path, config in state_json.items():
        relpath = os.path.relpath(path, root)
        split_path = relpath.split(os.sep)[1:]
        module_paths.append(split_path)
    return {
        'paths': module_paths
    }

def command_module(path):
    pass