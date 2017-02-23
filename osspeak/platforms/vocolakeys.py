### 
### Module Keys
### 

from platforms import dragonkeys
from platforms import sendinput

def send_input(specification):
    keys = dragonkeys.senddragonkeys_to_events(specification)
    sendinput.send_input(keys)

