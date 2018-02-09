import json
import inspect

def hello(*a, **kw):
    return 'hello'
resources = {
    'hello': hello
}


ws = None

async def gui_websocket_handler(websocket, path):
    print(websocket)
    while True:
        msg_string = await websocket.recv()
        msg = json.loads(msg_string)
        resource_function = resources[msg['resource']]
        data = resource_function(*msg['args'], **msg['kwargs'])
        if inspect.iscoroutinefunction(resource_function):
            data = await data
        response = json.dumps({
            'id': msg['id'],
            'data': data,
            'ok': True
        })
        await websocket.send(response)
    