### 
### Module Keys
### 

from recognition.actions.library.vocola import dragonkeys, sendinput

def send_input(specification):
    keys = dragonkeys.senddragonkeys_to_events(specification)
    sendinput.send_input(keys)
