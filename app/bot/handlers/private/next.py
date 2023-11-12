from datetime import datetime
from typing import Iterable, Optional, Tuple

from aiogram.types import Message

from app.messages.events import NEXT_EVENT
from app.services.schedule_api import ScheduleAPI
from app.services.types.general_event import GeneralEvent
from app.services.user_api import UserAPI
from app.utils.events import group_by_time


async def next_command(message: Message) -> None:
    async with UserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    async with ScheduleAPI() as schedule_api:
        general_events = await schedule_api.get_general_group_events_by_day(user.group.id, user_id=user.id)

    time = datetime.utcnow()
    next_time: Optional[Tuple[datetime, datetime]] = None
    next_events: Iterable[GeneralEvent] = []
    for (start_time, end_time), events in group_by_time(general_events.events):
        if start_time > time:
            next_time = (start_time, end_time)
            next_events = events
            break

    await message.answer(
        await NEXT_EVENT.render_async(events=next_events, time=next_time),
        disable_web_page_preview=True
    )
