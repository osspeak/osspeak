import json
import traceback
import inspect
from interfaces.gui.resources import commands

resources = {
    'RECOGNITION_INDEX': commands.recognition_index,
}

ws = None

async def gui_websocket_handler(websocket, path):
    while True:
        msg_string = await websocket.recv()
        response = await get_resource(msg_string)
        await websocket.send(response)

async def get_resource(msg: str):
    ok = True
    try:
        msg_data = json.loads(msg)
    except json.JSONDecodeError:
        ok = False
        data = f'Unable to decode JSON: {msg}'
    else:
        try:
            resource_function = resources[msg_data['resource']]
            data = await resource_function(*msg_data['args'], **msg_data['kwargs'])
        except Exception as e:
            traceback.print_exc()
            print('resource error')
            ok = False
            data = str(e)
    response = json.dumps({
        'id': msg_data['id'],
        'data': data,
        'ok': ok
    })
    return response
    