from osspeak.communication.engines import ProcessManager

class MessageDispatcher:

    def __init__(self):
        pass

    def cleanup(self):
        pass

    def process_received_message(self, msg):
        split_message = msg.strip().split(' ')
        if split_message[0] == 'result':
            action = self.cmd_module_loader.actions[split_message[1]]
            action.perform()

class MultipleProcessMessageDispatcher(MessageDispatcher):
    pass

class SingleProcessMessageDispatcher(MessageDispatcher):
    
    def __init__(self):
        self.engine_communicator = ProcessManager(self)
        self.engine_communicator.start_stdout_listening()

    def message_engine(self, msg):
        self.engine_communicator.send_message(msg)

    def send_message(self, msg):
        self.process_received_message(msg)