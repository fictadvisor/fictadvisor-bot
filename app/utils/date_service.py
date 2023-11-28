import math
from datetime import date, datetime

import pytz


class DateService:
    START_SEMESTER = date(2023, 9, 3).timetuple().tm_yday

    @staticmethod
    def get_now():
        return datetime.now(pytz.timezone("Europe/Kiev"))

    @classmethod
    def get_current_day(cls) -> int:
        return cls.get_now().date().timetuple().tm_yday - cls.START_SEMESTER

    @classmethod
    def get_current_weekday(cls) -> int:
        return cls.get_now().date().timetuple().tm_wday

    @staticmethod
    def get_week_by_day(day: int) -> int:
        return math.ceil(day / 7)

    @classmethod
    def get_week(cls) -> int:
        return math.ceil(cls.get_current_day() / 7)

    @staticmethod
    def add_tz_offset(time: datetime) -> datetime:
        return time.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone("Europe/Kiev"))
