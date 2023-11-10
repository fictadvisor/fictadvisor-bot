from datetime import datetime
from typing import Iterable, Optional, Tuple

from aiogram.types import Message

from app.messages.events import NEXT_EVENT
from app.services.schedule_api import ScheduleAPI
from app.services.types.general_event import GeneralEvent
from app.services.telegram_group_api import TelegramGroupAPI
from app.utils.events import group_by_time
from app.utils.date_service import DateService


async def next_command(message: Message) -> None:
    async with TelegramGroupAPI() as telegram_group_api:
        telegram_groups = await telegram_group_api.get_by_telegram_id(message.chat.id)
    for telegram_group in telegram_groups.telegram_groups:
        async with ScheduleAPI() as schedule_api:
            general_events = await schedule_api.get_general_group_events_by_day(telegram_group.group.id,
                                                                                day=DateService.get_current_day())

    time = datetime.utcnow()
    next_time: Optional[Tuple[int, int, int, int]] = None
    next_events: Iterable[GeneralEvent] = []
    for (start_hour, start_minute, end_hour, end_minute), events in group_by_time(general_events.events):
        if (start_hour == time.hour and start_minute > time.minute) or (start_hour > time.hour):
            next_time = (start_hour, start_minute, end_hour, end_minute)
            next_events = events
            break

    if not next_time:
        await message.answer("Сьогодні більше немає пар")
        return

    await message.answer(
        await NEXT_EVENT.render_async(events=next_events, time=next_time),
        disable_web_page_preview=True
    )
