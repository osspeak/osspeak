import json
import socket
from communication import pubsub
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
        else:
            return

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
    '''
    tasks must be in a separate thread, otherwise this just blocks forever
    '''
    remaining_tasks = tasks
    while remaining_tasks:
        next_remaining_tasks = []
        for task in remaining_tasks:
            if not task.done():
                next_remaining_tasks.append(task)
        remaining_tasks = next_remaining_tasks

def publish_json_message(msg):
    decoded_message = json.loads(msg)
    messages = decoded_message if isinstance(decoded_message, list) else [decoded_message]
    for message in messages:
        args = message.get('args', [])
        kwargs = message.get('kwargs', {})
        pubsub.publish(message['topic'], *args, **kwargs)

def get_host_and_port(address):
    host, port = address.rsplit(':', 1)
    return host, int(port)

async def receive_ws_messages(ws):
    while True:
        try:
            msg = await asyncio.wait_for(ws.recv(), timeout=20)
        except asyncio.TimeoutError:
            # No data in 20 seconds, check the connection.
            try:
                pong_waiter = await ws.ping()
                await asyncio.wait_for(pong_waiter, timeout=10)
            except asyncio.TimeoutError:
                # No response to ping in 10 seconds, disconnect.
                break
        else:
            publish_json_message(msg)