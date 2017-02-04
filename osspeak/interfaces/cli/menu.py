from communication import messages

class Menu:

    is_main_menu = True

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
            if result == 'quit':
                return
            if result:
                self.main_loop()

    def print_options(self):
        for i, option in enumerate(self.options, start=1):
            print(f'{i}. {option["text"]}')

class MainMenu(Menu):
    def __init__(self):
        self.options = [
            {'text': 'Debug commands', 'on_select': self.on_debug_commands},
            {'text': 'Adjust settings', 'on_select': self.on_adjust_settings}
        ]

    def on_debug_commands(self):
        messages.dispatch('engine stop')
        while True:
            user_input = input('Enter text to test or press enter to go back: ')
            if user_input:
                 messages.dispatch('emulate recognition', user_input)
            else:
                return

    def on_adjust_settings(self):
        messages.dispatch('engine stop')
        SettingsMenu().main_loop()


class SettingsMenu(Menu):
    
    def __init__(self):
        self.options = [
            {'text': 'Change remote server address', 'on_select': self.change_server_address},
        ]

    def change_server_address(self):
        print('csa')