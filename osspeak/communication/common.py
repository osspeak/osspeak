import json
from log import logger
from communication import messages

def receive_message(msg):
    message_object = msg if instance(msg, str) else json.loads(msg)
    messages.dispatch(message_object['name'], *message_object['args'], **message_object['kwargs'])

def send_message(ws, msg_name, *args, **kwargs):
    msg = {
        'name': msg_name,
        'args': args,
        'kwargs': kwargs,
    }
    ws.send_str(json.dumps(msg))

