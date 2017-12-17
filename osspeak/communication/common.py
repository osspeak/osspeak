import copy
import json
import socket
import queue
import queue
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

def put_message_in_queue(q, msg):
    while True:
        try:
            q.put_nowait(msg)
        except queue.Full as e:
            if not q.maxsize:
                raise e
            try:
                q.get_nowait()
            except queue.Empty:
                pass

def yield_queue_contents(q):
    while True:
        try:
            yield q.get_nowait()
        except queue.Empty:
            return

def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

def finish_tasks(tasks):
    remaining_tasks = tasks
    while remaining_tasks:
        next_remaining_tasks = []
        for task in remaining_tasks:
            if not task.done():
                next_remaining_tasks.append(task)
        remaining_tasks = next_remaining_tasks

def publish_json_message(msg):
    decoded_message = json.loads(msg)
    args = decoded_message.get('args', [])
    kwargs = decoded_message.get('kwargs', {})
    pubsub.publish(decoded_message.topic, *args, **kwargs)