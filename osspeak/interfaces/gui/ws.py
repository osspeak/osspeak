resources = {
    
}

ws = None

async def gui_websocket_handler(websocket, path):
    while True:
        msg = websocket.recv()
    print(websocket)
    