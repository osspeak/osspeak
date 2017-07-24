import contextlib
import time

@contextlib.contextmanager
def timer(name='timer'):
    start = time.clock()
    yield
    end = time.clock()
    print(f'{name}: {end - start} seconds')