import contextlib
import collections
import time

class Profiler:

    _active_profilers = {}

    def __init__(self, name=None):
        self.name = name
        self.start_time = None
        self.stop_time = None
        self._pieces = collections.OrderedDict()

    def start(self):
        if self.start_time is not None:
            raise RuntimeError('Profiler already started')
        if self.name is not None:
            self._active_profilers[self.name] = self
        self.start_time = time.time()

    def stop(self):
        stop_time = time.time()
        if self.stop_time is not None:
            raise RuntimeError('Profiler already stopped')
        if self.name is not None:
            del self._active_profilers[self.name]
        self.stop_time = stop_time

    def __enter__(self):
        self.start()

    def __exit__(self, *a, **kw):
        self.stop()
        self.dump()

    @property
    def running(self):
        return self.start_time is not None and self.stop_time is None

    def dump(self):
        from log import logger
        msg = []
        msg.append(f'\nProfiler "{self.name}":')
        msg.append(f'\tTotal time elapsed: {self.stop_time - self.start_time}')
        for name, piece_info in self._pieces.items():
            msg.append(f"\t\t{name}: {piece_info['total_time_elapsed']}")
        logger.debug('\n'.join(msg))

    @classmethod
    def get(cls, name):
        return cls._active_profilers[name]

    @contextlib.contextmanager
    def piece(self, name):
        if not self.running:
            raise RuntimeError('')
        start_time = time.time()
        yield
        stop_time = time.time()
        piece = self._pieces.get(name, empty_piece())
        piece['count'] += 1
        piece['total_time_elapsed'] += stop_time - start_time
        self._pieces[name] = piece
        
        
def empty_piece():
    return {
        'count': 0,
        'total_time_elapsed': 0
    }