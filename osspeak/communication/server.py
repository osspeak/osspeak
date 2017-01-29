import socket
import asyncio
import time
from communication import procs

# class RemoteEngineServer:

#     def __init__(self):
#         self.loop = asyncio.get_event_loop()
#         self.engine = procs.EngineProcessManager(remote=True)

#     def loop_forever(self):
#         # Each client connection will create a new protocol instance
        
#         coro = self.loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
#         self.server = self.loop.run_until_complete(coro)

#         # Serve requests until Ctrl+C is pressed
#         print('Serving on {}'.format(self.server.sockets[0].getsockname()))
#         try:
#             self.loop.run_forever()
#         except KeyboardInterrupt:
#             print('foo')
#         self.shutdown()

#     def shutdown(self):
#         # Close the server
#         self.server.close()
#         self.loop.run_until_complete(server.wait_closed())
#         self.loop.close()


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        print('Send: {!r}'.format(message))
        self.transport.write(data)
        print('Close the client socket')
        self.transport.close()
        asyncio.get_event_loop().stop()

    
    
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

class RemoteEngineServer:

    def loop_forever(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        print('Connection address:', addr)
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            print("received data:", data)
            conn.send(data)  # echo
            break
        conn.close()