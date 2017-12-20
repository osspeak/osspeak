import argparse
import __main__

def get_args():
    # return None for build script
    # TODO: better way to check main module?
    if __main__.__file__ == 'buildit.py':
        return
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', default=Nil)
    parser.add_argument('--network', default=Nil) # or remote
    parser.add_argument('--server_address', default=Nil)
    parser.add_argument('--type_delay', default=Nil)
    parser.add_argument('--debug', default=Nil, action='store_true')
    res = vars(parser.parse_args())
    return {k: v for (k, v) in res.items() if v is not Nil}

class Nil:
    pass