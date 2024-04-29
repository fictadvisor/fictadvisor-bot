from enum import Enum


class EventPeriod(str, Enum):
    EVERY_WEEK = "EVERY_WEEK"
    EVERY_FORTNIGHT = "EVERY_FORTNIGHT"
    NO_PERIOD = "NO_PERIOD"
