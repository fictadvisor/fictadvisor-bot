from aiogram.types import Message

from app.messages.events import EVENT_LIST
from app.services.schedule_api import ScheduleAPI
from app.services.user_api import UserAPI
from app.utils.date_service import DateService


async def tomorrow(message: Message) -> None:
    async with UserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    async with ScheduleAPI() as schedule_api:
        general_events = await schedule_api.get_general_group_events_by_day(user.group.id, DateService.get_current_day() + 1)

    if not general_events.events:
        await message.answer("Пар немає")
        return

    await message.answer(
        await EVENT_LIST.render_async(events=general_events.events),
        disable_web_page_preview=True
    )
