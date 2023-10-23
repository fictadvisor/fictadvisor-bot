from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.types.select_week import SelectWeek
from app.bot.keyboards.week_keyboard import get_week_keyboard
from app.messages.events import WEEK_EVENT_LIST
from app.services.schedule_api import ScheduleAPI
from app.services.telegram_group_api import TelegramGroupAPI
from app.utils.date_service import DateService
from app.utils.events import check_odd


async def fortnight(message: Message) -> None:
    async with TelegramGroupAPI() as telegram_group_api:
        telegram_groups = await telegram_group_api.get_by_telegram_id(message.chat.id)
    for telegram_group in telegram_groups.telegram_groups:
        async with ScheduleAPI() as schedule_api:
            general_events = await schedule_api.get_general_group_events_by_fortnight(telegram_group.group.id)

        week = 2 if check_odd(DateService.get_week()) else 1
        if not general_events.first_week_events and not general_events.second_week_events:
            await message.reply(f"У групи {telegram_group.group.code} пар немає")
        else:
            await message.reply(
                await WEEK_EVENT_LIST.render_async(group=telegram_group.group.code, events=(general_events.first_week_events, general_events.second_week_events)[week - 1], week=week),
                reply_markup=get_week_keyboard(week, telegram_group.group.id),
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
