from datetime import datetime, timedelta
from typing import Iterable, Optional, Tuple

import pytz
from aiogram.types import Message

from app.messages.events import NOW_EVENT
from app.services.schedule_api import ScheduleAPI
from app.services.types.general_event import GeneralEvent
from app.services.types.telegram_groups import TelegramGroupsByTelegramId
from app.utils.date_service import DateService
from app.utils.events import group_by_time


async def now_command(message: Message, telegram_groups: TelegramGroupsByTelegramId) -> None:
    for telegram_group in telegram_groups.telegram_groups:
        async with ScheduleAPI() as schedule_api:
            general_events = await schedule_api.get_general_group_events_by_day(telegram_group.group.id)

        if not general_events.events:
            await message.reply(f"У групи {telegram_group.group.code} пар немає")
            return

        now_time: Optional[Tuple[datetime, datetime]] = None
        now_events: Iterable[GeneralEvent] = []
        time = datetime.now(tz=pytz.UTC)
        time_left: Optional[timedelta] = None
        for (start_time, end_time), events in group_by_time(general_events.events):
            if start_time <= time <= end_time:
                time_left = end_time - time
                now_events = events
                now_time = (
                    DateService.add_tz_offset(start_time),
                    DateService.add_tz_offset(end_time)
                )
                break

        if not time_left:
            await message.reply(f"У групи {telegram_group.group.code} зараз пар немає")
            return

        await message.reply(
            await NOW_EVENT.render_async(group=telegram_group.group.code, events=now_events, event_time=now_time, time_left=(time_left.seconds//3600, time_left.seconds % 3600 // 60)),
            disable_web_page_preview=True
        )
