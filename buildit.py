import subprocess
import sys
import shutil
import os
import unittest
import json
import getpass
import requests
import zipfile
import io
import tempfile
import time

from osspeak import version

OSSPEAK_MAIN_PATH = os.path.join('osspeak', 'main.py')
OSSPEAK_SRC_FOLDER = 'osspeak'

DIST_FOLDER = 'dist'
BASE_ELECTRON_FOLDER = 'gui'
ELECTRON_BUILD_PATH = os.path.join('node_modules', 'electron', 'dist', 'resources', 'app')
ELECTRON_DIST_SRC = os.path.join('node_modules', 'electron', 'dist')

WSR_SRC_FOLDER = r'engines\RecognizerIO\RecognizerIO\bin\Debug'
WSR_DEST_FOLDER = os.path.join(DIST_FOLDER, 'engines', 'wsr')

TEST_DIR = os.path.join('osspeak', 'tests')

API_URL = 'https://github.com/api/v3/repos/osspeak/osspeak/releases'
UPLOAD_URL = 'https://github.com/api/uploads/repos/osspeak/osspeak/releases'


def main():
    tests_passed = run_tests()
    if not tests_passed:
        print('Unit test(s) failed')
        return
    # build_osspeak()
    create_github_release()
    # build_gui()

def build_gui():
    start_dir = os.getcwd()
    os.chdir(BASE_ELECTRON_FOLDER)
    for entry in os.scandir():
        if entry.is_dir() and entry.name == 'node_modules':
            continue
        dest = os.path.join(ELECTRON_BUILD_PATH, entry.name)
        if entry.is_dir():
            if not os.path.exists(dest):
                os.makedirs(dest)
            shutil.copytree(entry.name, dest)
        else:
            shutil.copyfile(entry.name, dest)
    dist_app = os.path.join('..', DIST_FOLDER, 'app')
    if os.path.exists(dist_app):
        shutil.rmtree(dist_app)
    shutil.copytree(ELECTRON_DIST_SRC, dist_app)
    os.chdir(start_dir)

def build_osspeak():
    subprocess.call(['pyinstaller', OSSPEAK_MAIN_PATH, '--clean', '-F',
    '--paths', OSSPEAK_SRC_FOLDER])
    copy_engines()

def copy_engines():
    if os.path.exists(WSR_DEST_FOLDER):
        shutil.rmtree(WSR_DEST_FOLDER)
    shutil.copytree(WSR_SRC_FOLDER, WSR_DEST_FOLDER)

def create_github_release():
    username = input('Github username: ')
    pwd = getpass.getpass('Github password: ')
    release_version = 'v{}'.format(version.version)
    auth = username, pwd
    data = {
        "tag_name": release_version,
        "name": release_version,
        "body": '\n'.join(version.release_notes),
    }
    response = requests.post(
        'https://api.github.com/repos/osspeak/osspeak/releases',
        data=json.dumps(data),
        auth=(username, pwd)
    )
    response_data = json.loads(response.text)
    upload_url = response_data['upload_url'].split('{')[0]
    upload_release_folder(upload_url, auth)

def run_tests():
    loader = unittest.TestLoader()
    test_suite = loader.discover(TEST_DIR, top_level_dir=OSSPEAK_SRC_FOLDER)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

def upload_release_folder(upload_url, auth, zip_name='windows-cli.zip'):
    fd, fname = tempfile.mkstemp(suffix='.zip')
    shutil.make_archive(fname[:-4], root_dir='dist', format='zip')
    with open(fname, 'rb') as f:
        zip_bytes = f.read()
    os.close(fd)
    os.remove(fname)
    headers = {
        'Content-Type': 'application/zip',
        'name': 'windows-cli.zip'
    }
    response = requests.post(
        upload_url + '?name={}'.format(zip_name),
        data=zip_bytes,
        auth=auth,
        headers=headers
    )

if __name__ == '__main__':
    main()