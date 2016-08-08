import os
import json

class CommandModuleHandler:

    def __init__(self):
        self.cmd_modules = {}

    def load_command_json(self):
        for root, dirs, filenames in os.walk(r'C:\Users\evan\modules\OSSpeak\user\commands'):
            for fname in filenames:
                full_path = os.path.join(root, fname)
                with open(full_path) as f:
                    self.cmd_modules[full_path] = json.load(f)
        print(self.cmd_modules)

    def send_grammar_load_messages(self, messenger):
        for path, cmd_module_json in self.cmd_modules.items():
            module_string = json.dumps(cmd_module_json)
            print('sending message')
            print('load_command_module {}'.format(module_string))
            messenger.send_message('load_command_module {}'.format(module_string))
