from datetime import datetime, timedelta
from typing import Optional

import pytz
from aiogram.types import Message

from app.messages.events import LEFT_EVENT
from app.services.schedule_api import ScheduleAPI
from app.services.types.telegram_groups import TelegramGroupsByTelegramId
from app.utils.events import group_by_time


async def left_command(message: Message, telegram_groups: TelegramGroupsByTelegramId) -> None:
    for telegram_group in telegram_groups.telegram_groups:
        async with ScheduleAPI() as schedule_api:
            general_events = await schedule_api.get_general_group_events_by_day(telegram_group.group.id)

        if not general_events.events:
            await message.reply(f"У групи {telegram_group.group.code} пар немає")
            return

        time = datetime.now(tz=pytz.UTC)
        time_left: Optional[timedelta] = None
        for (start_time, end_time), _events in group_by_time(general_events.events):
            if start_time <= time <= end_time:
                time_left = end_time - time
                break

        if not time_left:
            await message.reply(f"У групи {telegram_group.group.code} зараз пар немає")
            return

        await message.reply(
            await LEFT_EVENT.render_async(group=telegram_group.group.code, time_left=(time_left.seconds//3600, time_left.seconds % 3600 // 60)),
            disable_web_page_preview=True
        )
