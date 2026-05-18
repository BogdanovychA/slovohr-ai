# -*- coding: utf-8 -*-

import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def api_timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            duration = end_time - start_time
            logger.info(f"API call to '{func.__name__}' took {duration:.4f} seconds")

    return wrapper
