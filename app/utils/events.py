from datetime import datetime
from itertools import groupby
from typing import Iterable, Iterator, List, Optional, Tuple, Union
from uuid import UUID

from app.services.types.general_event import GeneralEvent
from app.services.types.general_events import FortnightGeneralEvents
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
    if DateService.get_current_weekday() == weekday:
        return f"{allocation} {weekdays[weekday]}"
    return f"⬜️⬜️⬜️ {weekdays[weekday]}"


def what_week_event(fortnight_general_event: FortnightGeneralEvents, event_id: Union[UUID, str]) -> int:
    week = DateService.get_week()
    if next(filter(lambda x: x.id == event_id, fortnight_general_event.first_week_events), None) and next(filter(lambda x: x.id == event_id, fortnight_general_event.second_week_events), None): # type: ignore[union-attr, arg-type]
        return week
    elif next(filter(lambda x: x.id == event_id, fortnight_general_event.first_week_events), None):
        return week + 1 if check_odd(week) else week
    else:
        return week if check_odd(week) else week + 1
