import math
from datetime import date, datetime, timezone


class DateService:
    START_SEMESTER = date(2023, 9, 3).timetuple().tm_yday

    @classmethod
    def get_current_day(cls) -> int:
        if 24 - datetime.now(tz=timezone.utc).time().hour <= 2:
            return date.today().timetuple().tm_yday - cls.START_SEMESTER + 1

        return date.today().timetuple().tm_yday - cls.START_SEMESTER

    @classmethod
    def get_week(cls) -> int:
        return math.ceil(cls.get_current_day() / 7)
