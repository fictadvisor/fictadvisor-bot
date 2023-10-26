from datetime import date
from itertools import groupby
from typing import Iterable, Iterator, List, Optional, Tuple

from app.services.types.general_event import GeneralEvent
from app.utils.date_service import DateService

weekdays = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця", "Субота", "Неділя"]


def check_odd(n: int) -> bool:
    return True if n % 2 == 0 else False


def group_by_time(
        events: List[GeneralEvent]
) -> Iterator[Tuple[Tuple[int, int, int, int], Iterable[GeneralEvent]]]:
    return groupby(events, lambda x: (x.start_time.hour, x.start_time.minute, x.end_time.hour, x.end_time.minute))


def group_by_weekday(
        events: List[GeneralEvent]
) -> Iterator[Tuple[int, Iterable[GeneralEvent]]]:
    return groupby(events, lambda x: x.start_time.weekday())


def get_weekday_name(weekday: int, week: Optional[int] = None) -> str:
    allocation = "🟥🟥🟥"
    if week and check_odd(week) != check_odd(DateService.get_week()):
        allocation = "⬜️⬜️⬜️"
    if date.today().weekday() == weekday:
        return f"{allocation} {weekdays[weekday]}"
    return f"⬜️⬜️⬜️ {weekdays[weekday]}"
