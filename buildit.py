import subprocess
import sys
import shutil
import os
import os.path
import unittest
import json
import getpass
import requests
import zipfile
import argparse
import io
import tempfile
import time
import lark

from osspeak import version


OSSPEAK_MAIN_PATH = os.path.join('osspeak', 'main.py')
OSSPEAK_SRC_FOLDER = 'osspeak'

DIST_FOLDER = 'dist'

WSR_SRC_FOLDER = os.path.join('engines', 'RecognizerIO', 'RecognizerIO', 'bin', 'Debug')
WSR_DEST_FOLDER = os.path.join(DIST_FOLDER, 'engines', 'wsr')

TEST_DIR = os.path.join('osspeak', 'tests')

API_URL = 'https://github.com/api/v3/repos/osspeak/osspeak/releases'
UPLOAD_URL = 'https://github.com/api/uploads/repos/osspeak/osspeak/releases'


def main():
    cl_args = parse_cl_args()
    # tests_passed = run_tests()
    # if not tests_passed:
    #     print('Unit test(s) failed')
    #     return
    build_osspeak()
    if cl_args.release:
        create_github_release()

def parse_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--release', action='store_true')
    return parser.parse_args()

def build_osspeak():
    lark_path = os.path.dirname(os.path.abspath(lark.__file__))
    grammar_path = os.path.join(lark_path, 'grammars', 'common.lark')
    dest_path = os.path.join('lark', 'grammars')
    subprocess.call(['pyinstaller', OSSPEAK_MAIN_PATH, '--clean', '-F',
    '--paths', OSSPEAK_SRC_FOLDER, '--add-data', f'{grammar_path};{dest_path}', '-n', 'osspeak'])
    copy_engines()

def copy_engines():
    if os.path.exists(WSR_DEST_FOLDER):
        shutil.rmtree(WSR_DEST_FOLDER)
    shutil.copytree(WSR_SRC_FOLDER, WSR_DEST_FOLDER)

def create_github_release():
    username = input('Github username: ')
    pwd = getpass.getpass('Github password: ')
    release_version = f'v{version.version}'
    auth = username, pwd
    data = {
        "tag_name": release_version,
        "name": release_version,
    }
    response = requests.post(
        'https://api.github.com/repos/osspeak/osspeak/releases',
        data=json.dumps(data),
        auth=auth
    )
    if not response.ok:
        print('Error uploading release to GitHub:')
        print(response.text)
        return
    response_data = json.loads(response.text)
    upload_url = response_data['upload_url'].split('{')[0]
    upload_release_folder(upload_url, auth)

def run_tests():
    loader = unittest.TestLoader()
    test_suite = loader.discover(TEST_DIR, top_level_dir=OSSPEAK_SRC_FOLDER)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

def upload_release_folder(upload_url, auth, zip_name='windows-cli.zip'):
    zip_bytes = write_release_zip()
    headers = {
        'Content-Type': 'application/zip',
        'name': 'windows-cli.zip'
    }
    response = requests.post(
        f'{upload_url}?name={zip_name}',
        data=zip_bytes,
        auth=auth,
        headers=headers
    )

def write_release_zip():
    fd, fname = tempfile.mkstemp(suffix='.zip')
    shutil.make_archive(fname[:-4], root_dir='dist', format='zip')
    with open(fname, 'rb') as f:
        zip_bytes = f.read()
    os.close(fd)
    os.remove(fname)
    return zip_bytes

if __name__ == '__main__':
    main()