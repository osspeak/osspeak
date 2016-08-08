import socket
import asyncore
from osspeak import defaults
import threading
import time
import socketserver

class OSSpeakServer(socketserver.TCPServer):

    def __init__(self, *a, **k):
        self.on_receive = k.pop('on_receive')
        self.socket_messenger = k.pop('socket_messenger')
        super().__init__(*a, **k)

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(16384).strip()
        self.server.on_receive(self.server, data)

class SocketMessenger:
    def __init__(self, host=socket.gethostname(), port=None,
                 other_host=socket.gethostname(), other_port=None,
                 on_cleanup=lambda: None, on_receive=lambda x, y: None):
        self.host = host
        self.port = port
        self.other_host = other_host
        self.other_port = other_port
        self.on_cleanup = on_cleanup
        self.on_receive = on_receive
        start_thread(self.start_listening_loop)

    def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.other_host, self.other_port))
            sock.sendall(msg)
            # received = str(sock.recv(1024), "utf-8")

    def start_listening_loop(self):
        self.tcp_server = OSSpeakServer((self.host, self.port), MyTCPHandler,
                                        on_receive=self.on_receive, socket_messenger=self)
        self.tcp_server.serve_forever()

    def cleanup(self):
        self.on_cleanup()        
        self.tcp_server.shutdown()

def start_thread(target, args=None):
    args = args or ()
    t = threading.Thread(target=target, args=args)
    t.start()
    return t