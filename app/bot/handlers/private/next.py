import logging
from datetime import datetime
from typing import Iterable, Optional, Tuple

import pytz
from aiogram.types import Message

from app.messages.events import NEXT_EVENT
from app.services.exceptions.response_exception import ResponseException
from app.services.schedule_api import ScheduleAPI
from app.services.types.general_event import GeneralEvent
from app.services.user_api import UserAPI
from app.utils.events import group_by_time
from app.utils.telegram import send_answer


async def next_command(message: Message) -> None:
    try:
        async with UserAPI() as user_api:
            user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    except ResponseException as e:
        await send_answer(message, "Прив'яжіть телеграм до аккаунта FICE Advisor")
        logging.error(e)
        return

    async with ScheduleAPI() as schedule_api:
        general_events = await schedule_api.get_general_group_events_by_day(user.group.id, user_id=user.id)

    if not general_events.events:
        await message.answer("Сьогодні пар немає")
        return

    time = datetime.now(tz=pytz.UTC)
    next_time: Optional[Tuple[datetime, datetime]] = None
    next_events: Iterable[GeneralEvent] = []
    for (start_time, end_time), events in group_by_time(general_events.events):
        if start_time > time:
            next_time = (start_time, end_time)
            next_events = events
            break

    if not next_time:
        await message.answer("Сьогодні більше немає пар")
        return

    await message.answer(
        await NEXT_EVENT.render_async(events=next_events, event_time=next_time),
        disable_web_page_preview=True
    )
