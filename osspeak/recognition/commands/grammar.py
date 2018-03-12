import uuid

class GrammarContext:
    
    def __init__(self, xml, command_contexts, active_commands, namespace, named_rules):
        self.xml = xml
        self.uuid = str(uuid.uuid4())
        self.command_contexts = command_contexts
        self.active_commands = active_commands 
        self.namespace = namespace
        self.named_rules = named_rules

        self.command_rules = [cmd.rule for cmd in active_commands]
        self.rule_to_command_map = {c.rule: c for c in active_commands}
