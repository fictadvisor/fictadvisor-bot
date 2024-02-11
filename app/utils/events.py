from datetime import datetime
from itertools import chain, groupby
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


def combine_events(fortnight_general_event: FortnightGeneralEvents) -> List[GeneralEvent]:
    first_week_ids: List[UUID] = [event.id for event in fortnight_general_event.first_week_events]
    second_week_ids: List[UUID] = [event.id for event in fortnight_general_event.second_week_events]

    unique_ids: List[UUID] = list(set(chain(first_week_ids, second_week_ids)))

    group_events: List[GeneralEvent] = [
        event for event in chain(fortnight_general_event.first_week_events, fortnight_general_event.second_week_events)
        if event.id in unique_ids
    ]
    return group_events


def what_week_event(fortnight_general_event: FortnightGeneralEvents, event_id: Union[UUID, str]) -> int:
    if next(filter(lambda x: x.id == event_id, fortnight_general_event.first_week_events), None) and next(filter(lambda x: x.id == event_id, fortnight_general_event.second_week_events), None):
        return 2 if check_odd(DateService.get_week()) else 1
    else:
        return 2 if next(filter(lambda x: x.id == event_id, fortnight_general_event.second_week_events), None) else 1
