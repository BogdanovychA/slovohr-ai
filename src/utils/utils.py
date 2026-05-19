# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import logging
import time
from functools import wraps

import yaml

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


def read_yaml_file(file: Path) -> dict[str, str]:

    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

    except FileNotFoundError as e:
        data = {}
        logger.warning("FileNotFoundError: %s", e)

    except Exception as e:
        data = {}
        logger.exception("Unexpected error: %s", e)

    return data


def clamp_value(
    value: int | float, min_value: int | float | None, max_value: int | float | None
) -> int | float:
    """Обмеження значення між min та max.
    Якщо щось обмежувати не треба -- передаємо None"""

    if min_value is not None:
        value = max(value, min_value)
    if max_value is not None:
        value = min(value, max_value)
    return value
