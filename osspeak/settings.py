import os
import logging
import json
import clargs
import sys

OSSPEAK_DIRECTORY = os.path.join(os.path.expanduser('~'), '.osspeak')
EXECUTABLE_DIRECTORY = os.path.split(os.path.abspath(sys.argv[0]))[0]
OSSPEAK_CONFIG_PATH = 'osspeak.json' if os.path.exists('osspeak.json') else os.path.join(OSSPEAK_DIRECTORY, 'osspeak.json')

DEFAULT_CONFIG = {
    'interface': 'cli',
    'network': 'local',
    'server_address': '127.0.0.1:8888',
    "type_delay": .05,
    'command_directory': os.path.join(OSSPEAK_DIRECTORY, 'commands'),
    'external_directory': os.path.join(OSSPEAK_DIRECTORY, 'external'),
    'cache': os.path.join(OSSPEAK_DIRECTORY, '.cache.json'),
    'macros': os.path.join(OSSPEAK_DIRECTORY, 'macros.json'),
    'print_logging_level': logging.INFO,
    'file_logging_level': logging.DEBUG,
    'gui_port': 3922,
    'perform_actions': True,
    'engine': {
        'recognitionConfidence': .9
    }
}

def try_load_json_file(path, default=dict):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return default() if callable(default) else default

def save_settings(settings):
    if not os.path.isdir(OSSPEAK_DIRECTORY):
        os.makedirs(OSSPEAK_DIRECTORY)
    with open(OSSPEAK_CONFIG_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

def load_user_settings():
    user_settings = DEFAULT_CONFIG.copy()
    user_settings.update(try_load_json_file(os.path.join(OSSPEAK_DIRECTORY, 'osspeak.json')))
    user_settings.update(try_load_json_file(os.path.join(EXECUTABLE_DIRECTORY, 'osspeak.json')))
    args = clargs.get_args()
    if args is not None:
        user_settings.update(args)
    return user_settings

try:
    settings = load_user_settings()
except:
    settings = DEFAULT_CONFIG.copy()

def get_server_address():
    address = settings['server_address'].rsplit(':', 1)
    return address[0], int(address[1])

def parse_server_address(address):
    if isinstance(address, str):
        return address
    if isinstance(address, dict) and 'host' in address and 'port' in address:
        return f'{address["host"]}:{address["port"]}'
