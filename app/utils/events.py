from datetime import date, datetime
from itertools import groupby
from typing import Iterable, Iterator, List, Optional, Tuple

from app.services.types.general_event import GeneralEvent
from app.utils.date_service import DateService

weekdays = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]


def check_odd(n: int) -> bool:
    return True if n % 2 == 0 else False


def group_by_time(
        events: List[GeneralEvent]
) -> Iterator[Tuple[Tuple[datetime, datetime], Iterable[GeneralEvent]]]:
    return groupby(events, lambda x: (x.start_time, x.end_time))


def group_by_weekday(
        events: List[GeneralEvent]
) -> Iterator[Tuple[int, Iterable[GeneralEvent]]]:
    return groupby(events, lambda x: x.start_time.weekday())


def get_weekday_name(weekday: int, week: Optional[int] = None) -> str:
    allocation = "🟥🟥🟥"
    if week and check_odd(week) != check_odd(DateService.get_week()):
        allocation = "⬜️⬜️⬜️"
    if DateService.get_current_wday() == weekday:
        return f"{allocation} {weekdays[weekday]}"
    return f"⬜️⬜️⬜️ {weekdays[weekday]}"
