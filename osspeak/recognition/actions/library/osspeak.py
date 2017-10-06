from communication import messages

def reload():
    messages.dispatch_sync(messages.RELOAD_COMMAND_MODULE_FILES)

