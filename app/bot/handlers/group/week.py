from aiogram.types import Message

from app.messages.events import WEEK_EVENT_LIST
from app.services.schedule_api import ScheduleAPI
from app.services.telegram_group_api import TelegramGroupAPI


async def week(message: Message) -> None:
    async with TelegramGroupAPI() as telegram_group_api:
        telegram_groups = await telegram_group_api.get_by_telegram_id(message.chat.id)
    for telegram_group in telegram_groups.telegram_groups:
        async with ScheduleAPI() as schedule_api:
            general_events = await schedule_api.get_general_group_events_by_week(telegram_group.group.id)

        if not general_events.events:
            await message.answer("Пар немає")
            return

        await message.reply(
            await WEEK_EVENT_LIST.render_async(events=general_events.events),
            disable_web_page_preview=True
        )
