import os
import json
from settings import defaults

OSSPEAK_DIRECTORY = os.path.join(os.path.expanduser('~'), '.osspeak')

def load_user_config():
    config_file_path = os.path.join(OSSPEAK_DIRECTORY, 'config.json')
    try:
        if not os.path.exists(config_file_path):
            with open(config_file_path, 'w') as f:
                json.dump(defaults.DEFAULT_CONFIG, f)
    except IndexError:
        pass
    try:
        with open(config_file_path) as f:
            user_config = json.load(f)
    except IndexError:
        user_config = defaults.DEFAULT_CONFIG
    return user_config

def command_directory():
    return defaults.COMMAND_DIRECTORY