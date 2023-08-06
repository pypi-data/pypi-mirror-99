import time
from functools import wraps


class MaxRetriesExceededError(Exception):
    pass


def retry(max_retries=3):
    def retry_dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    attempt += 1
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries:
                        time.sleep(attempt)
                    else:
                        errmsg = "{}() failed after {} retries".format(
                            func.__name__, max_retries
                        )
                        raise MaxRetriesExceededError(errmsg) from e

        return wrapper

    return retry_dec
