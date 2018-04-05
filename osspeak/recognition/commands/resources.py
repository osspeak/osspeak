import os
from settings import settings
from recognition.commands import monitor

def command_modules():
    state = monitor.command_module_state.command_module_json
    root = settings['command_directory']
    module_paths = []
    for path, config in state.items():
        relpath = os.path.relpath(path, root)
        split_path = relpath.split(os.sep)[1:]
        module_paths.append(split_path)
    return {
        'module_paths': module_paths
    }