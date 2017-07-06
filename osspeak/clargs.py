import argparse
import __main__

def get_args():
    # return None for build script
    # TODO: better way to check main module?
    if __main__.__file__ == 'buildit.py':
        return
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--interface', default='remote')
    parser.add_argument('--network', default='local') # or remote
    parser.add_argument('--engine_server', action='store_true')
    return parser.parse_args()