import argparse
import shutil
import requests
import sys
from io import BytesIO
from zipfile import ZipFile
import os
import __main__

STANDALONE_APPLICATIONS = 'standalone_applications'
GET_PIP_URL = 'https://bootstrap.pypa.io/get-pip.py'

MAIN_BATCH_SCRIPT = '''
@echo off
cd osspeak && ..\\python\\python.exe main.py %* & cd .. && pause
'''

def try_makedirs(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

def try_remove_directory(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

def main():
    args = get_args()
    name = args['name']
    version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
    application_dir = os.path.join(STANDALONE_APPLICATIONS, name)
    try_remove_directory(application_dir)
    resp = requests.get(f'https://www.python.org/ftp/python/{version}/python-{version}-embed-amd64.zip')
    python_dir = os.path.join(application_dir, 'python')
    try_makedirs(python_dir)
    with ZipFile(BytesIO(resp.content)) as my_zip_file:
        for contained_file in my_zip_file.namelist():
            full_path = os.path.join(python_dir, contained_file)
            with open(full_path, 'wb') as f:
                with my_zip_file.open(contained_file) as zip_piece_file:
                    f.write(zip_piece_file.read())
            print(contained_file)
    build_dir = os.path.join(application_dir, 'build')
    try_makedirs(build_dir)
    with open(os.path.join(build_dir, 'get-pip.py'), 'wb') as f:
        resp = requests.get(GET_PIP_URL)
        f.write(resp.content)
            # with open(("unzipped_and_read_" + contained_file + ".file"), "wb") as output:
            # for line in my_zip_file.open(contained_file).readlines():
            #     print(line)
    shutil.copytree('osspeak', os.path.join(application_dir, 'osspeak'))
    with open(os.path.join(application_dir, f'{name}.bat'), 'w') as f:
        f.write(MAIN_BATCH_SCRIPT)

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
    parser.add_argument('name', help='Application name', type=str)
    parser.add_argument('-i', '--interface', default=Nil)
    parser.add_argument('--network', default=Nil) # or remote
    parser.add_argument('--server_address', default=Nil)
    parser.add_argument('--type_delay', default=Nil)
    parser.add_argument('-f', '--file_pattern', default='', help='File pattern for command modules')
    parser.add_argument('--clean_cache', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Clear out command module cache")
    parser.add_argument('-t', '--text_mode', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Start in text mode")
    parser.add_argument('-a', '--perform_actions', type=str2bool, nargs='?',
                        const=True, default=True,
                        help="Perform recognized speech actions")
    parser.add_argument('--debug', default=Nil, action='store_true')
    res = vars(parser.parse_args())
    return {k: v for (k, v) in res.items() if v is not Nil}

class Nil:
    pass

if __name__ == "__main__":
    main()