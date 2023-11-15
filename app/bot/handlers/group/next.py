from datetime import datetime
from typing import Iterable, Optional, Tuple

import pytz
from aiogram.types import Message

from app.messages.events import NEXT_EVENT
from app.services.schedule_api import ScheduleAPI
from app.services.types.general_event import GeneralEvent
from app.services.types.telegram_groups import TelegramGroupsByTelegramId
from app.utils.date_service import DateService
from app.utils.events import group_by_time


async def next_command(message: Message, telegram_groups: TelegramGroupsByTelegramId) -> None:
    for telegram_group in telegram_groups.telegram_groups:
        async with ScheduleAPI() as schedule_api:
            general_events = await schedule_api.get_general_group_events_by_day(telegram_group.group.id, day=DateService.get_current_day())

        if not general_events.events:
            await message.reply("Сьогодні пар немає")
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
            await message.reply(f"Сьогодні у групи {telegram_group.group.code} більше немає пар")
            return

        await message.reply(
            await NEXT_EVENT.render_async(events=next_events, event_time=next_time),
            disable_web_page_preview=True
        )
