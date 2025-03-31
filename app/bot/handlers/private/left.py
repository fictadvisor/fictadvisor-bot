import logging
from datetime import datetime, timedelta
from typing import Optional

import pytz
from aiogram.types import Message

from app.messages.events import LEFT_EVENT
from app.services.exceptions.response_exception import ResponseException
from app.services.schedule_api import ScheduleAPI
from app.services.user_api import UserAPI
from app.utils.events import group_by_time
from app.utils.telegram import send_answer


async def left_command(message: Message) -> None:
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
    time_left: Optional[timedelta] = None
    for (start_time, end_time), _events in group_by_time(general_events.events):
        if start_time <= time <= end_time:
            time_left = end_time - time
            break

    if not time_left:
        await message.answer("Зараз немає пар")
        return

    await message.answer(
        await LEFT_EVENT.render_async(time_left=(time_left.seconds//3600, time_left.seconds % 3600 // 60)),
        disable_web_page_preview=True
    )
