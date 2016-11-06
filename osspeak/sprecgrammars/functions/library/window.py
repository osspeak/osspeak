from platforms import api

def focus(title):
    print('tt', title)
    api.activate_window(title)

def close():
    api.close_active_window()