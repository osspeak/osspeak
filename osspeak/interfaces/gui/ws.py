import json
import traceback
import functools
import inspect
from interfaces.gui.resources import commands
from communication import topics, pubsub, server

ws = None

resources = {
    topics.RECOGNITION_INDEX: commands.recognition_index,
    'SAVE_MODULE_CHANGES': commands.save_module_changes
}

def resource_coroutine(topic):
    async def resource(*a, **kw):
        if ws is None:
            return
        data = await resources[topic](*a, **kw)
        msg = json.dumps({'topic': topic, 'data': data})
        await ws.send(msg)
    return resource

for topic in resources:
    coro = resource_coroutine(topic)
    pubsub.subscribe(topic, coro)

async def gui_websocket_handler(websocket, path):
    global ws
    ws = websocket
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
    