from communication import topics, pubsub

def reload():
    pubsub.publish(topics.RELOAD_COMMAND_MODULE_FILES)

