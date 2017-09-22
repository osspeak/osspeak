import time
import os
import subprocess

def wait(duration=0):
    time.sleep(float(duration))

def proc(cmd, block=False):
    if isinstance(cmd, str):
        cmd = cmd.split()
    p = subprocess.Popen(cmd, shell=True)

def path(p):
    return os.path.normpath(p)