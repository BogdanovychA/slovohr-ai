# -*- coding: utf-8 -*-

from enum import StrEnum


class LoggingLevel(StrEnum):
    """Доступні рівні логування для програми."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EventName(StrEnum):
    ROUTE_CHANGE = "route_change"
    QUERY_SENT = "query_sent"


class Analytics(StrEnum):
    NO_PLATFORM = "no_platform"
