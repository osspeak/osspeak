import uuid

class GrammarContext:
    
    def __init__(self, xml, command_contexts):
        self.xml = xml
        self.uuid = str(uuid.uuid4())
        self.command_contexts = command_contexts
