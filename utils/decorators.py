import time

from tqdm import tqdm


def retry(times, exceptions, delay=0):
    def decorator(func):
        def _fn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    tqdm.write(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt += 1
                    time.sleep(delay)

            return func(*args, **kwargs)
        return _fn
    return decorator
