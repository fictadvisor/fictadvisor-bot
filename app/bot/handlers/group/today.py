from aiogram.types import Message

from app.messages.events import EVENT_LIST
from app.services.schedule_api import ScheduleAPI
from app.services.types.telegram_groups import TelegramGroupsByTelegramId


async def today(message: Message, telegram_groups: TelegramGroupsByTelegramId) -> None:
    for telegram_group in telegram_groups.telegram_groups:
        async with ScheduleAPI() as schedule_api:
            general_events = await schedule_api.get_general_group_events_by_day(telegram_group.group.id)

        if not general_events.events:
            await message.reply(f"У групи {telegram_group.group.code} пар немає")
        else:
            await message.reply(
                await EVENT_LIST.render_async(group=telegram_group.group.code, events=general_events.events),
                disable_web_page_preview=True
            )
