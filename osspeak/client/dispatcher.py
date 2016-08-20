from osspeak.communication.engines import SpeechEngineCommunicator

class MessageDispatcher:

    def __init__(self):
        pass

    def cleanup(self):
        pass

    def process_received_message(self, msg):
        pass

class MultipleProcessMessageDispatcher(MessageDispatcher):
    pass

class SingleProcessMessageDispatcher(MessageDispatcher):
    
    def __init__(self):
        self.engine_communicator = SpeechEngineCommunicator(self)
        self.engine_communicator.start_engine_listening()

    def message_engine(self, msg):
        self.engine_communicator.send_message(msg)

    def send_message(self, msg):
        pass