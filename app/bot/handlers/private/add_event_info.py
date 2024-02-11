from contextlib import suppress
from typing import Union
from uuid import UUID
from app.services.types.general_event import VerifyEvent

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.event_info_keyboards import (
    get_events_dates,
    get_events_filter_keyboard,
    get_events_keyboard
)
from app.services.types.student import Student
from app.bot.keyboards.types.event_info import EventFilter, SelectDate, SelectEvent
from app.services.schedule_api import ScheduleAPI
from app.services.types.certain_event import CertainEvent
from app.services.types.general_events import FortnightGeneralEvents
from app.services.user_api import UserAPI
from app.utils.date_service import DateService
from app.utils.events import combine_events, what_week_event
from app.utils.get_discipline_type_name import get_discipline_type_name
from aiogram.fsm.context import FSMContext


async def add_homework_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    async with UserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(message.from_user.id) # type: ignore[union-attr]
    async with ScheduleAPI() as schedule_api:
        fortnight_general_events: FortnightGeneralEvents = await schedule_api.get_general_group_events_by_fortnight(group_id=user.group.id, user_id=user.id)

    if not fortnight_general_events.first_week_events and not fortnight_general_events.second_week_events:
        await message.answer("На найближчий час пар немає")
        return
    
    group_events = combine_events(fortnight_general_events)
    
    await state.set_data({"user": user, "fortnight_general_events": fortnight_general_events})

    await message.answer(
        text="Вибери пару на яку хочеш додати дз\n\n🔵 Лекція 🟠 Практика 🟢 Лаба 🟣 Консультація",
        reply_markup=get_events_keyboard(group_events, message.from_user.id)
    )
    await message.answer(
        text=f"Фільтрувати по: {message.message_id}",
        reply_markup=get_events_filter_keyboard(tgid=message.from_user.id)
    )


async def filter_event(callback: CallbackQuery, callback_data: EventFilter, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    user: Student = data.get("user")
    group_events = combine_events(data.get("fortnight_general_events"))
    
    with suppress(TelegramBadRequest):
        await bot.edit_message_reply_markup(
            user.telegram_id, callback.message.message_id - 1,
            reply_markup=get_events_keyboard(group_events, user.telegram_id, callback_data.type)
        )
    await callback.answer()


async def cancel_select_event(callback: CallbackQuery, bot: Bot, state: FSMContext):
    for i in range(2):
        await bot.delete_message(callback.data.split(":")[1], callback.message.message_id + i)
    await callback.message.answer("Відміняю")
    await state.clear()


async def select_event(callback: CallbackQuery, callback_data: SelectEvent, bot: Bot, state: FSMContext) -> None:
    await state.update_data({"event_id": callback_data.event_id})
    data = await state.get_data()
    user: Student = data.get("user")
    fortnight_general_events: FortnightGeneralEvents = data.get("fortnight_general_events")
    
    await callback.message.answer(
        text=f"group_id: {user.group.id}\nevent_id: {callback_data.event_id}\nweek: {DateService.get_week()}"
    )
    
    week = what_week_event(fortnight_general_events, callback_data.event_id)
    await callback.message.answer(f"week at end: {week}")
    async with ScheduleAPI() as schedule_api:
        certain_event: CertainEvent = await schedule_api.get_certain_event(callback_data.event_id, user.group.id, week=week)
        
    await state.update_data({"certain_event": certain_event})

    for i in range(2):
        await bot.delete_message(user.telegram_id, callback.message.message_id + i)
    
    await callback.message.answer(
        text=f"{get_discipline_type_name(certain_event.discipline_type)} {certain_event.name}\nНа коли хочете додати дз?\nНайближча пара:",
        reply_markup=get_events_dates(event=certain_event)
    )
    await callback.answer()
    
    
async def refresh_dates(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    user: Student = data.get("user")
    certain_event: CertainEvent = data.get("certain_event")
    event_id: Union[UUID, str] = data.get("event_id")
    await bot.edit_message_reply_markup(
            user.telegram_id, callback.message.message_id - 1,
            reply_markup=get_events_dates(certain_event, user.telegram_id, event_id, callback.data.split(":")[1])
        )

async def select_date(callback: CallbackQuery, callback_data: SelectDate, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    user: Student = data.get("user")
    fortnight_general_events: FortnightGeneralEvents = data.get("fortnight_general_events")
    certain_event: CertainEvent = data.get("certain_event")
    

    await callback.answer()


async def add_event_info(event_id: Union[UUID, str], group_id: Union[UUID, str], data: VerifyEvent) -> None:
    async with ScheduleAPI() as schedule_api:
        await schedule_api.add_event_info(event_id=event_id, group_id=group_id, data=data)
