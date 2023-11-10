from aiogram.types import Message

from app.messages.events import NOW_EVENT
from app.services.schedule_api import ScheduleAPI
from app.services.user_api import UserAPI
from app.utils.date_service import DateService


async def now(message: Message) -> None:
    async with UserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    async with ScheduleAPI() as schedule_api:
        general_events = await schedule_api.get_general_group_events_by_day(user.group.id, user_id=user.id, day=DateService.get_current_day() + 1)

    if not general_events.events:
        await message.answer("Пар немає")
        return
    
    if general_events.events:
        for event in (general_events.events):
            if(event.start_time < DateService.get_utcnow() < event.end_time):
                await message.answer(
                    await NOW_EVENT.render_async(event=event),
                    disable_web_page_preview=True
                )