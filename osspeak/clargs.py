import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--interface', default='remote')
    parser.add_argument('--network', default='local') # or remote
    parser.add_argument('--engine_server', action='store_true')
    return parser.parse_args()

args = get_args()