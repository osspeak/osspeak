import os
import json

OSSPEAK_DIRECTORY = os.path.join(os.path.expanduser('~'), '.osspeak')
USER_DIRECTORY = os.path.join(OSSPEAK_DIRECTORY, 'user')
COMMAND_DIRECTORY = os.path.join(USER_DIRECTORY, 'commands')
DEFAULT_CONFIG = {
    'interface': 'cli',
    'network': 'local',
    'server_address': '127.0.0.1:8888',
    "type_delay": .05,
}

def load_user_settings():
    config_file_path = os.path.join(OSSPEAK_DIRECTORY, 'config.json')
    if not os.path.exists(config_file_path):
        save_settings(DEFAULT_CONFIG)
    try:
        with open(config_file_path) as f:
            user_settings = json.load(f)
    except json.decoder.JSONDecodeError:
        # logger.warning('Invalid settings configuration. Loading default settings.')
        user_settings = DEFAULT_CONFIG
    for setting_name in DEFAULT_CONFIG:
        user_settings[setting_name] = user_settings.get(setting_name, DEFAULT_CONFIG[setting_name])
    return user_settings

user_settings = load_user_settings()

def save_settings(settings):
    if not os.path.isdir(OSSPEAK_DIRECTORY):
        os.makedirs(OSSPEAK_DIRECTORY)
    config_file_path = os.path.join(OSSPEAK_DIRECTORY, 'config.json')
    with open(config_file_path, 'w') as f:
        json.dump(settings, f, indent=4)

def command_directory():
    return defaults.COMMAND_DIRECTORY

def parse_server_address(address):
    if isinstance(address, str):
        return address
    if isinstance(address, dict) and 'host' in address and 'port' in address:
        return f'{address["host"]}:{address["port"]}'