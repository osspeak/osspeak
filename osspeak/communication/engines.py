import subprocess
import threading

ENGINE_PATH = r'C:\Users\evan\modules\OSSpeak\engines\RecognizerIO\RecognizerIO\bin\Debug\RecognizerIO.exe'

class SpeechEngineCommunicator:

    def __init__(self, dispatcher):
        self.engine_process = subprocess.Popen(ENGINE_PATH, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.dispatcher = dispatcher
        

    def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
            self.engine_process.stdin.write(msg)
            self.engine_process.stdin.flush()

    def dispatch_engine_output(self):
        for line in self.engine_process.stdout:
            print(line)
            line = line.decode('utf8')
            self.dispatcher.send_message(line)

    def start_engine_listening(self):
        t = threading.Thread(target=self.dispatch_engine_output)
        t.start()