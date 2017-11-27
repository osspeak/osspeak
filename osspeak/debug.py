import contextlib
import time

@contextlib.contextmanager
def timer(name='timer'):
    start = time.clock()
    yield
    end = time.clock()
    print(f'{name}: {end - start} seconds')

class Timer:

    active_timers = {}

    def __init__(self, name=None):
        self.name = name
        if name is not None:
            active_timers[name] = self
        self.start_time = None
        self.sections = {}

    def start(self):
        self.start_time = time.time()

    def stop(self):
        stop_time = time.time()

with Timer.get('foo').section('tokenize')