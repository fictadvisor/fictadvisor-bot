from datetime import datetime
from typing import Iterable, Optional, Tuple

from aiogram.types import Message

from app.messages.events import NOW_EVENT
from app.services.schedule_api import ScheduleAPI
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.general_event import GeneralEvent
from app.utils.events import group_by_time


async def now_command(message: Message) -> None:
    async with TelegramGroupAPI() as telegram_group_api:
        telegram_groups = await telegram_group_api.get_by_telegram_id(message.chat.id)
    for telegram_group in telegram_groups.telegram_groups:
        async with ScheduleAPI() as schedule_api:
            general_events = await schedule_api.get_general_group_events_by_day(telegram_group.group.id)

        if not general_events.events:
            await message.reply(f"У групи {telegram_group.group.code} пар немає")
        else:
            time = datetime.utcnow()
            now_time: Optional[Tuple[int, int, int, int]] = None
            now_event: Iterable[GeneralEvent] = []
            time_left: Optional[Tuple[int, int]] = None
            for (start_hour, start_minute, end_hour, end_minute), events in group_by_time(general_events.events):
                if (start_hour <= time.hour <= end_hour) and (start_minute < time.minute < end_minute):
                    now_time = (start_hour, start_minute, end_hour, end_minute)
                    now_event = events
                    if (end_minute - start_minute) < 0:
                        time_left = (end_hour - start_hour - 1, end_minute - start_minute + 60)
                    else:
                        time_left = (end_hour - start_hour, end_minute - start_minute)
                    break

        await message.reply(
            await NOW_EVENT.render_async(group=telegram_group.group.code, events=now_event, event_time=now_time, time_left=time_left),
            disable_web_page_preview=True
        )
