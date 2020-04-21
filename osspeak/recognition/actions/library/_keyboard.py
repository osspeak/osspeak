import threading
import re
from lib import keyboard
from recognition.actions.library.vocola import dragonkeys, sendinput
from platforms import api
import time
import threading

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
        unpressed_chords = []
        for i, chord in enumerate(self.chords):
            is_last_chord = i + 1 == len(self.chords)
            chord_keys = keys_pressed_from_chord(chord)
            delay = key_delayer.delays.get(chord_keys)
            time_to_wait = delay.time_to_wait if delay else 0
            if time_to_wait:
                send_chords(unpressed_chords)
                time.sleep(delay.time_to_wait)
                unpressed_chords = [chord]
            else:
                unpressed_chords.append(chord)
            if is_last_chord:
                send_chords(unpressed_chords)
            if delay:
                delay.reset()

def send_chords(chords):
    if not chords:
        return
    events = events_from_chords(chords)
    sendinput.send_input(events)

def events_from_chords(chords):
    events = []
    for chord in chords:
        chord_events = dragonkeys.chord_to_events(chord)
        events.extend(chord_events)
    return events

class DelayTimer:

    def __init__(self, length):
        self.length = length
        self.start = None

    def reset(self):
        self.start = time.time()

    @property
    def time_to_wait(self):
        if self.start is None:
            return 0
        now = time.time()
        done_at = self.start + self.length
        return max(done_at - now, 0)

class KeyDelayer:

    def __init__(self):
        self.delays = {}

    def add_delay(self, keys, n):
        delay = DelayTimer(n)
        for key_combo in keys:
            self.delays[key_combo] = delay

    def remove_delay(self, keys):
        for key_combo in keys:
            try:
                del self.delays[key_combo]
            except KeyError:
                pass

key_delayer = KeyDelayer()

def add_delay(context, keys, n):
    keys = keys.evaluate(context)
    n = n.evaluate(context)
    all_keys = expand_keys(keys)
    key_delayer.add_delay(all_keys, n)

def remove_delay(context, keys):
    keys = keys.evaluate(context)
    all_keys = expand_keys(keys)
    key_delayer.remove_delay(all_keys)

def expand_keys(keys):
    if not isinstance(keys, (list, tuple)):
        keys = [keys]
    all_keys = []
    for value in keys:
        if isinstance(value, re.Pattern):
            for known_key in dragonkeys.Key_name:
                if value.match(known_key):
                    key_tuple = known_key,
                    if key_tuple not in all_keys:
                        all_keys.append(key_tuple)
        elif isinstance(value, str):
            key_tuple = value,
            if key_tuple not in all_keys:
                all_keys.append(key_tuple)
        else:
            raise NotImplementedError
    return all_keys

def keys_pressed_from_chord(chord):
    first = [] if chord[0] in (None, '') else chord[0].split('+')
    return tuple(x.lower() for x in first + [chord[1]])