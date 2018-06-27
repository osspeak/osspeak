import json
import traceback
import inspect
from recognition.commands import resources as command_resources

resources = {
    'RECOGNITION_INDEX': command_resources.recognition_index,
}

ws = None

async def gui_websocket_handler(websocket, path):
    while True:
        msg_string = await websocket.recv()
        ok = True
        try:
            msg = json.loads(msg_string)
        except json.JSONDecodeError:
            ok = False
            data = f'Unable to decode JSON: {msg_string}'
        else:
            try:
                resource_function = resources[msg['resource']]
                data = resource_function(*msg['args'], **msg['kwargs'])
                if inspect.iscoroutinefunction(resource_function):
                    data = await data
            except Exception as e:
                traceback.print_exc()
                print('resource error')
                ok = False
                data = str(e)
        response = json.dumps({
            'id': msg['id'],
            'data': data,
            'ok': ok
        })
        await websocket.send(response)
    