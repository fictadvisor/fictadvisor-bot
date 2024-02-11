from aiogram.types import Message

from app.messages.events import EVENT_INFOS_LIST
from app.services.schedule_api import ScheduleAPI
from app.services.user_api import UserAPI
from app.utils.date_service import DateService


async def today_events_infos_command(message: Message) -> None:
    async with UserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    async with ScheduleAPI() as schedule_api:
        general_events = await schedule_api.get_general_group_events_by_day(user.group.id, user_id=user.id, day=3, week=7)

    await message.answer(f"{DateService.get_current_day()}")
    if not general_events.events:
        await message.answer("Пар немає")
        return

    for event in general_events.events:
        if event.event_info:
            await message.answer(
                await EVENT_INFOS_LIST.render_async(events=general_events.events),
                disable_web_page_preview=True
            )
            return

    await message.answer("ДЗ немає")
