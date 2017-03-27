import collections

command_history = collections.deque(maxlen=100)

def last():
    commands = command_history[-1]
    for command in commands:
        command['action'].perform(command['variables'])

def get(index):
    return command_history(index)