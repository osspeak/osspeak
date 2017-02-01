import os
import json

OSSPEAK_DIRECTORY = os.path.join(os.path.expanduser('~'), '.osspeak')
USER_DIRECTORY = os.path.join(OSSPEAK_DIRECTORY, 'user')
COMMAND_DIRECTORY = os.path.join(USER_DIRECTORY, 'commands')
DEFAULT_CONFIG = {
    'interface': 'cli',
    'engine_server': False,
    'network': 'local',
    'server_address': {
        'host': '127.0.0.1',
        'port': 8888,
    }
}

def load_user_settings():
    # from log import logger
    if not os.path.isdir(OSSPEAK_DIRECTORY):
        os.mkdir(OSSPEAK_DIRECTORY)
    config_file_path = os.path.join(OSSPEAK_DIRECTORY, 'config.json')
    try:
        if not os.path.exists(config_file_path):
            with open(config_file_path, 'w') as f:
                json.dump(DEFAULT_CONFIG, f)
    except IndexError:
        pass
    try:
        with open(config_file_path) as f:
            user_settings = json.load(f)
    except IndexError:
        # logger.warning('Invalid settings configuration. Loading default settings.')
        user_settings = DEFAULT_CONFIG
    for setting_name in DEFAULT_CONFIG:
        user_settings[setting_name] = user_settings.get(setting_name, DEFAULT_CONFIG[setting_name])
    return user_settings

user_settings = load_user_settings()

def command_directory():
    return defaults.COMMAND_DIRECTORY