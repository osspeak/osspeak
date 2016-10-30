import subprocess
import sys
import shutil
import os

OSSPEAK_MAIN_PATH = os.path.join('osspeak', 'main.py')
OSSPEAK_SRC_FOLDER = 'osspeak'

DIST_FOLDER = 'dist'
BASE_ELECTRON_FOLDER = 'gui'
ELECTRON_BUILD_PATH = os.path.join('node_modules', 'electron', 'dist', 'resources', 'app')
ELECTRON_DIST_SRC = os.path.join('node_modules', 'electron', 'dist')

WSR_SRC_FOLDER = r'engines\RecognizerIO\RecognizerIO\bin\Debug'
WSR_DEST_FOLDER = os.path.join(DIST_FOLDER, 'engines', 'wsr')

def main():
    build_osspeak()
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

if __name__ == '__main__':
    main()