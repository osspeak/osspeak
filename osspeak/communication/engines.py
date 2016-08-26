import subprocess
import threading

ENGINE_PATH = r'C:\Users\evan\modules\OSSpeak\engines\RecognizerIO\RecognizerIO\bin\Debug\RecognizerIO.exe'

class ProcessManager:

    def __init__(self, dispatcher, on_output=lambda x: None):
        self.process = subprocess.Popen(ENGINE_PATH, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.dispatcher = dispatcher
        self.on_output = on_output
        

    def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
            self.process.stdin.write(msg)
            self.process.stdin.flush()

    def dispatch_process_output(self):
        for line in self.process.stdout:
            line = line.decode('utf8')
            self.on_output(line)
            self.dispatcher.send_message(line)

    def start_stdout_listening(self):
        t = threading.Thread(target=self.dispatch_process_output)
        t.start()