from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.types.select_week import SelectWeek
from app.bot.keyboards.week_keyboard import get_week_keyboard
from app.messages.events import WEEK_EVENT_LIST
from app.services.schedule_api import ScheduleAPI
from app.services.user_api import UserAPI
from app.utils.date_service import DateService
from app.utils.events import check_odd


async def fortnight(message: Message) -> None:
    async with UserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    async with ScheduleAPI() as schedule_api:
        general_events = await schedule_api.get_general_group_events_by_fortnight(user.group.id)

    if not general_events.first_week_events and not general_events.second_week_events:
        await message.answer("Пар немає")
        return

    week = 2 if check_odd(DateService.get_week()) else 1
    await message.answer(
        await WEEK_EVENT_LIST.render_async(events=(general_events.first_week_events, general_events.second_week_events)[week - 1], week=week),
        reply_markup=get_week_keyboard(week, user.group.id),
        disable_web_page_preview=True
    )


async def select_week(callback: CallbackQuery, callback_data: SelectWeek) -> None:
    async with ScheduleAPI() as schedule_api:
        general_events = await schedule_api.get_general_group_events_by_fortnight(callback_data.group_id)
    week = callback_data.week

    await callback.message.edit_text(  # type: ignore[union-attr]
        await WEEK_EVENT_LIST.render_async(events=(general_events.first_week_events, general_events.second_week_events)[week - 1], week=week),
        reply_markup=get_week_keyboard(week, callback_data.group_id),
        disable_web_page_preview=True
    )
