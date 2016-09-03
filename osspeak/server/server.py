import socket
import sys
import subprocess
import time
from functools import partial
from asyncio.subprocess import PIPE
sys.path.append("..") 
from osspeak import protocols, defaults
from server import handlers
import threading

ENGINE_PATH = r'C:\Users\evan\modules\OSSpeak\engines\RecognizerIO\RecognizerIO\bin\Debug\RecognizerIO.exe'
DEFAULT_PORT_NUMBER = 8301

def dispatch_engine_output(engine_process, messenger):
    return
    for line in engine_process.stdout:
        line = line.decode('utf8')
        messenger.send_message(line)

def main():
    try:
        engine_process = subprocess.Popen(ENGINE_PATH, stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NEW_CONSOLE)
        dispatch_func = partial(handlers.dispatch_message_from_client, engine_process)
        s = protocols.SocketMessenger(port=defaults.SERVER_PORT, other_port=defaults.CLIENT_PORT,
                                      on_cleanup=engine_process.kill,
                                      on_receive=dispatch_func)
        t = threading.Thread(target=dispatch_engine_output, args=(engine_process, s))
        t.start()
        x = input('toast :').encode('utf8')
        engine_process.stdin.write(x + b'\n')
        engine_process.stdin.flush()
        while True:
            time.sleep(1)
    finally:
        s.cleanup()



if __name__ == "__main__":
    main()