import math
from datetime import datetime

import pytz


class DateService:
    TIMEZONE = pytz.timezone("Europe/Kiev")
    START_SEMESTER = datetime(2023, 9, 3, tzinfo=TIMEZONE)

    @classmethod
    def get_now(cls) -> datetime:
        return datetime.now(cls.TIMEZONE)

    @classmethod
    def get_current_day(cls) -> int:
        return (cls.get_now() - cls.START_SEMESTER).days

    @classmethod
    def get_current_weekday(cls) -> int:
        return cls.get_now().date().timetuple().tm_wday

    @staticmethod
    def get_week_by_day(day: int) -> int:
        return math.ceil(day / 7)

    @classmethod
    def get_week(cls) -> int:
        return math.ceil(cls.get_current_day() / 7)

    @classmethod
    def add_tz_offset(cls, time: datetime) -> datetime:
        return time.replace(tzinfo=pytz.UTC).astimezone(cls.TIMEZONE)
