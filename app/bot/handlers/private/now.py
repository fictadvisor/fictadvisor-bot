import logging
from datetime import datetime, timedelta
from typing import Iterable, Optional, Tuple

import pytz
from aiogram.types import Message

from app.messages.events import NOW_EVENT
from app.services.exceptions.response_exception import ResponseException
from app.services.schedule_api import ScheduleAPI
from app.services.types.general_event import GeneralEvent
from app.services.user_api import UserAPI
from app.utils.events import group_by_time
from app.utils.telegram import send_answer


async def now_command(message: Message) -> None:
    try:
        async with UserAPI() as user_api:
            user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    except ResponseException as e:
        await send_answer(message, "Прив'яжіть телеграм до аккаунта FICE Advisor")
        logging.error(e)
        return

    async with ScheduleAPI() as schedule_api:
        general_events = await schedule_api.get_general_group_events_by_day(user.group.id, user_id=user.id)

    now_time: Optional[Tuple[datetime, datetime]] = None
    now_events: Iterable[GeneralEvent] = []
    time = datetime.now(tz=pytz.UTC)
    time_left: Optional[timedelta] = None
    for (start_time, end_time), events in group_by_time(general_events.events):
        if start_time <= time <= end_time:
            time_left = end_time - time
            now_events = events
            now_time = (start_time, end_time)
            break

    if not time_left:
        await message.answer("Зараз немає пари")
        return

    await message.answer(
        await NOW_EVENT.render_async(events=now_events, event_time=now_time, time_left=(time_left.seconds//3600, time_left.seconds % 3600 // 60)),
        disable_web_page_preview=True
    )
