from communication import messages
from user import settings

class Menu:

    def main_loop(self, display_options=True):
        if display_options:
            self.print_title()
            self.print_options()
        user_input = input("\nEnter an option or 'q' to quit: ").strip().lower()
        if user_input == 'q':
            return
        if not user_input:
            return True
        try:
            option = self.options[int(user_input) - 1]
        except (ValueError, IndexError):
            print('Did not understand input')
            self.main_loop(display_options=False)
        else:
            result = option['on_select']()
            if result:
                return self.main_loop()

    def print_title(self):
        print('\n' + self.title)
        print('==============')

    def print_options(self):
        print('')
        for i, option in enumerate(self.options, start=1):
            print(f'{i}. {option["text"]}')

class MainMenu(Menu):
    def __init__(self):
        self.title = 'Main Menu'
        self.options = [
            {'text': 'Debug commands', 'on_select': self.on_debug_commands},
            {'text': 'Adjust settings', 'on_select': self.on_adjust_settings},
            {'text': 'Reload command modules', 'on_select': self.reload_command_modules},
        ]

    def on_debug_commands(self):
        messages.dispatch_sync(messages.ENGINE_STOP)
        while True:
            user_input = input('Enter text to test or press enter to go back: ')
            if user_input:
                 messages.dispatch_sync(messages.EMULATE_RECOGNITION, user_input)
            else:
                messages.dispatch_sync(messages.ENGINE_START)
                return True

    def on_adjust_settings(self):
        messages.dispatch(messages.ENGINE_STOP)
        return SettingsMenu().main_loop()

    def reload_command_modules(self):
        print('Reloading command modules...')
        messages.dispatch(messages.RELOAD_COMMAND_MODULE_FILES)
        return True

class SettingsMenu(Menu):
    
    def __init__(self):
        self.title = 'Settings'
        self.options = [
            {'text': 'Display current settings', 'on_select': self.display_current_settings},
            {'text': 'Change interface', 'on_select': self.change_server_address},
            {'text': 'Change network mode', 'on_select': self.change_server_address},
            {'text': 'Change remote server address', 'on_select': self.change_server_address},
        ]

    def change_server_address(self):
        address_input = input('Enter new remote server address: ')
        if address_input:
            # address:port
            split_input = address_input.split(':')
            if len(split_input) != 2 or '' in split_input:
                print('invalid host:port combination')
            else:
                host, port = split_input
                settings.user_settings['server_address'] = address_input
                print(f'Saving new remote server address: {address_input}')
                settings.save_settings(settings.user_settings)
        return True

    def display_current_settings(self):
        print('\nCurrent settings: ')
        ui = 'command line' if settings.user_settings['interface'] else 'GUI'
        print(f'User interface: {ui}')
        network_mode = {'server': 'Speech engine server', 'remote': 'Remote client'}.get(settings.user_settings['network'], 'Local')
        print(f'Network mode: {network_mode}')
        engine_server = settings.parse_server_address(settings.user_settings['server_address'])
        if engine_server is None:
            engine_server = 'Invalid'
        print (f'Speech engine server address (not used in local mode): {engine_server}')
        return True