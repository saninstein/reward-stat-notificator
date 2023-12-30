import logging
from datetime import timedelta
from typing import Callable

import retrying


def get_class_logger(obj):
    """
    Get the logger for the given class or object's class.
    """
    klass = obj if isinstance(obj, type) else obj.__class__
    return logging.getLogger(f'{klass.__module__}.{klass.__name__}')


@retrying.retry(wait_exponential_multiplier=500, wait_exponential_max=10000, stop_max_attempt_number=5)
def retry_call(call: Callable):
    """
    Retries on exception
    """
    return call()


def readable_timedelta(duration: timedelta) -> str:
    """
    Returns a timedelta in humanreadable format
    """
    data = {}
    data['d'], remaining = divmod(duration.total_seconds(), 86_400)
    data['h'], remaining = divmod(remaining, 3_600)
    data['m'], data['s'] = divmod(remaining, 60)

    time_parts = ((name, round(value)) for name, value in data.items())
    time_parts = [f'{value}{name[:-1] if value == 1 else name}' for name, value in time_parts if value > 0]
    if time_parts:
        return ' '.join(time_parts)
    else:
        return 'below 1s'
