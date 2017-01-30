TERMINATION_SEQUENCE = 'f1a5238b-ec60-430e-a0a8-5fe7442273a0'

def send_message(self, socket, msg_name, *args, **kwargs):
    msg = {
        'name': msg_name,
        'args': args,
        'kwargs': kwargs,
    }
    encoded_message = json.dumps(msg)
    msg_bytes = bytes(f'{encoded_message}\n', 'utf-8')
    socket.sendall(msg_bytes)