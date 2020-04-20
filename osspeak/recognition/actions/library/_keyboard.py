import threading
from lib import keyboard
from recognition.actions.library.vocola import dragonkeys, sendinput
from platforms import api
import time
import threading

shortcuts = {
    'back': 'backspace'
}

class KeyPress:

    def __init__(self, chords):
        self.chords = chords

    @classmethod
    def from_raw_text(cls, s: str):
        chords = []
        for char in s:
            chords.append([None, char, None, char])
        instance = cls(chords)
        return instance

    @classmethod
    def from_space_delimited_string(cls, s: str):
        spl = s.split(' ')
        specification = '{' + '+'.join(spl) + '}'
        chords = dragonkeys.parse_into_chords(specification)
        instance = cls(chords)
        return instance

    def send(self):
        events = []
        for chord in self.chords:
            keys_pressed = keys_pressed_from_chord(chord)
            chord_events = dragonkeys.chord_to_events(chord)
            events.extend(chord_events)
        sendinput.send_input(events)

class KeyDelayer:

    def __init__(self):
        self.delays_by_key = {}
        self.last_keypresses = {}

key_delayer = KeyDelayer()

def add_delay():
    pass

def keys_pressed_from_chord(chord):
    first = [] if chord[0] is None else chord[0].split('+')
    return tuple(first + [chord[1]])