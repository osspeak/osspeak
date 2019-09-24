import argparse
import __main__

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1', True):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', False):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_args():
    # return None for build script
    # TODO: better way to check main module?
    if __main__.__file__ == 'buildit.py':
        return
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', default=Nil)
    parser.add_argument('--network', default=Nil) # or remote
    parser.add_argument('--server_address', default=Nil)
    parser.add_argument('--type_delay', default=Nil)
    parser.add_argument('--clean_cache', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Perform recognized speech actions")
    parser.add_argument('-a', '--perform_actions', type=str2bool, nargs='?',
                        const=True, default=True,
                        help="Perform recognized speech actions")
    parser.add_argument('--debug', default=Nil, action='store_true')
    res = vars(parser.parse_args())
    return {k: v for (k, v) in res.items() if v is not Nil}

class Nil:
    pass