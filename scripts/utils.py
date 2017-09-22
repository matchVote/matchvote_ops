from contextlib import contextmanager
import sys


@contextmanager
def log(message):
    print(message, end='')
    sys.stdout.flush()
    yield
    print('Done')
