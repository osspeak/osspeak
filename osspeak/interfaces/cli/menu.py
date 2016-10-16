class Menu:

    def __init__(self, event_dispatcher):
        self.init_options()
        self.event_dispatcher = event_dispatcher

    def prompt_input(self, display_options=True):
        self.print_options()
        user_input = input("\nEnter an option or 'q' to quit: ").strip().lower()
        if user_input == 'q':
            return
        try:
            option = self.options[int(user_input) - 1]
        except (ValueError, IndexError):
            print('Did not understand input\n')
            self.prompt_input(display_options=False)
        else:
            result = option['on_select']()
            if result:
                self.prompt_input()

    def init_options(self):
        self.options = [
            {'text': 'Debug commands', 'on_select': self.on_debug_commands}
        ]

    def on_debug_commands(self):
        self.event_dispatcher.engine_process.stop()
        while True:
            user_input = input('Enter text to test or press enter to go back: ')
            if user_input:
                self.event_dispatcher.engine_process.emulate_recognition(user_input)
            else:
                return

    def print_options(self):
        for i, option in enumerate(self.options, start=1):
            print('{}. {}'.format(i, option['text']))

class MenuOption:
    pass