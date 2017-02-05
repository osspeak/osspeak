import os

OSSPEAK_DIRECTORY = os.path.join(os.path.expanduser('~'), '.osspeak')

USER_DIRECTORY = os.path.join(OSSPEAK_DIRECTORY, 'user')

COMMAND_DIRECTORY = os.path.join(USER_DIRECTORY, 'commands')

DEFAULT_CONFIG = {
    'interface': 'cli',
    'network': 'local',
    'server_address': {
        'ip': '127.0.0.1',
        'port': 8888,
    }
}