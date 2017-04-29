import subprocess
import threading

class ProcessManager:

    def __init__(self, path, on_output=lambda x: None):
        self.process = subprocess.Popen(path, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        self.on_output = on_output
        self.start_stdout_listening()
        
    def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
        self.process.stdin.write(msg)
        try:
            self.process.stdin.flush()
        except OSError:
            print(f'Process {self} already closed')

    def dispatch_process_output(self):
        for line in self.process.stdout:
            line = line.decode('utf8')
            self.on_output(line)

    def start_stdout_listening(self):
        t = threading.Thread(target=self.dispatch_process_output, daemon=True)
        t.start()

