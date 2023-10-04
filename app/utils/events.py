from itertools import groupby
from typing import Iterable, Iterator, List, Tuple

from app.services.types.general_event import GeneralEvent

weekdays = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця", "Субота", "Неділя"]


def group_by_time(
        events: List[GeneralEvent]
) -> Iterator[Tuple[Tuple[int, int, int, int], Iterable[GeneralEvent]]]:
    return groupby(events, lambda x: (x.start_time.hour, x.start_time.minute, x.end_time.hour, x.end_time.minute))


def group_by_weekday(
        events: List[GeneralEvent]
) -> Iterator[Tuple[int, Iterable[GeneralEvent]]]:
    return groupby(events, lambda x: x.start_time.weekday())


def get_weekday_name(weekday: int) -> str:
    return weekdays[weekday]
