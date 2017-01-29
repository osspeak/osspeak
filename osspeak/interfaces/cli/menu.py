from communication import messages

class Menu:

    def __init__(self):
        self.init_options()

    def main_loop(self, display_options=True):
        self.print_options()
        user_input = input("\nEnter an option or 'q' to quit: ").strip().lower()
        if user_input == 'q':
            return
        try:
            option = self.options[int(user_input) - 1]
        except (ValueError, IndexError):
            print('Did not understand input\n')
            self.main_loop(display_options=False)
        else:
            result = option['on_select']()
            if result:
                self.main_loop()

    def init_options(self):
        self.options = [
            {'text': 'Debug commands', 'on_select': self.on_debug_commands}
        ]

    def on_debug_commands(self):
        messages.dispatch('engine stop')
        while True:
            user_input = input('Enter text to test or press enter to go back: ')
            if user_input:
                 messages.dispatch('emulate recognition', user_input)
            else:
                return

    def print_options(self):
        for i, option in enumerate(self.options, start=1):
            print('{}. {}'.format(i, option['text']))

    def send_message(self, msgkey, payload):
        pass

class MenuOption:
    pass