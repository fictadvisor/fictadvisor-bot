import math
from datetime import date, datetime

import pytz


class DateService:
    START_SEMESTER = date(2023, 9, 3).timetuple().tm_yday

    @classmethod
    def get_current_day(cls) -> int:
        return datetime.now(pytz.timezone("Europe/Kiev")).date().timetuple().tm_yday - cls.START_SEMESTER

    @classmethod
    def get_current_weekday(cls) -> int:
        return datetime.now(pytz.timezone("Europe/Kiev")).date().timetuple().tm_wday

    @classmethod
    def get_week(cls) -> int:
        return math.ceil(cls.get_current_day() / 7)

    @staticmethod
    def add_tz_offset(time: datetime) -> datetime:
        return time.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone("Europe/Kiev"))
