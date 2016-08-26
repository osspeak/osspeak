import subprocess
import sys
import shutil
import os

OSSPEAK_MAIN_PATH = os.path.join('osspeak', 'client', 'client.py')
DIST_FOLDER = 'dist'
BASE_ELECTRON_FOLDER = 'gui'
ELECTRON_BUILD_PATH = os.path.join('node_modules', 'electron', 'dist', 'resources', 'app')
ELECTRON_DIST_SRC = os.path.join('node_modules', 'electron', 'dist')

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
    subprocess.call(['pyinstaller', OSSPEAK_MAIN_PATH, '--clean', '-F'])

if __name__ == '__main__':
    main()