from contextlib import suppress
from typing import List, Union
from uuid import UUID

from aiogram import Bot
from aiogram.enums.content_type import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.event_info_keyboards import (
    get_approve,
    get_events_dates,
    get_events_filter_keyboard,
    get_events_keyboard,
)
from app.bot.keyboards.types.event_info import EventFilter, SelectDate, SelectEvent
from app.bot.states.event_info_states import AddEventInfoStates
from app.messages.events import VERIFY_EVENT_INFO
from app.services.schedule_api import ScheduleAPI
from app.services.types.certain_event import CertainEvent
from app.services.types.general_event import GeneralEvent, VerifyEvent
from app.services.types.general_events import FortnightGeneralEvents
from app.services.types.student import Student
from app.services.user_api import UserAPI
from app.utils.discipline_type import get_discipline_type_color
from app.utils.events import what_week_event


async def add_info_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    async with UserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(message.from_user.id) # type: ignore[union-attr]
    async with ScheduleAPI() as schedule_api:
        fortnight_general_events: FortnightGeneralEvents = await schedule_api.get_general_group_events_by_fortnight(group_id=user.group.id, user_id=user.id)

    if not fortnight_general_events.first_week_events and not fortnight_general_events.second_week_events:
        await message.answer("На найближчий час пар немає")
        return

    all_group_events = fortnight_general_events.first_week_events + fortnight_general_events.second_week_events
    all_unique_group_events: List[GeneralEvent] = sorted(set(all_group_events))

    await state.set_data({"user": user, "fortnight_general_events": fortnight_general_events, "all_unique_group_events": all_unique_group_events})

    await message.answer(
        text="Вибери пару на яку хочеш додати інформацію\n\n🔵 Лекція 🟠 Практика 🟢 Лаба 🟣 Консультація",
        reply_markup=get_events_keyboard(all_unique_group_events)
    )
    await message.answer(
        text="Фільтрувати по:",
        reply_markup=get_events_filter_keyboard()
    )


async def filter_event(callback: CallbackQuery, callback_data: EventFilter, bot: Bot, state: FSMContext) -> None:
    if callback.message:
        data = await state.get_data()
        user: Student = data.get("user") # type: ignore[assignment]
        all_unique_group_events: List[GeneralEvent] = data.get("all_unique_group_events") # type: ignore[assignment]

        with suppress(TelegramBadRequest):
            await bot.edit_message_reply_markup(
                user.telegram_id, callback.message.message_id - 1,
                reply_markup=get_events_keyboard(all_unique_group_events, callback_data.type)
            )
        await callback.answer()


async def cancel(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if callback.message:
        user: Student = (await state.get_data()).get("user") # type: ignore[assignment]
        if callback.data == "event_cancel":
            for i in range(2):
                await bot.delete_message(user.telegram_id, callback.message.message_id + i) # type: ignore[arg-type]
        elif callback.data == "date_cancel":
            await callback.message.delete()
        await callback.message.answer("Відміняю 🚫")
        await state.clear()


async def select_event(callback: CallbackQuery, callback_data: SelectEvent, bot: Bot, state: FSMContext) -> None:
    if callback.message:
        await state.update_data({"event_id": callback_data.event_id})
        data = await state.get_data()
        user: Student = data.get("user") # type: ignore[assignment]
        fortnight_general_events: FortnightGeneralEvents = data.get("fortnight_general_events") # type: ignore[assignment]

        week = what_week_event(fortnight_general_events, callback_data.event_id)
        async with ScheduleAPI() as schedule_api:
            certain_event: CertainEvent = await schedule_api.get_certain_event(callback_data.event_id, user.group.id, week=week)

        await state.update_data({"certain_event": certain_event})

        await callback.message.delete()

        await bot.edit_message_text(
            text=f"{get_discipline_type_color(certain_event.discipline_type)} {certain_event.name}\nНа коли хочете додати інформацію?\nНайближчі пари в порядку зростання:",
            chat_id=user.telegram_id,
            message_id=callback.message.message_id + 1,
            reply_markup=get_events_dates(event=certain_event, week=week)
        )
        await callback.answer()


async def refresh_dates(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if callback.message and callback.data:
        data = await state.get_data()
        certain_event: CertainEvent = data.get("certain_event") # type: ignore[assignment]
        await callback.message.edit_reply_markup(
                reply_markup=get_events_dates(certain_event, week=int(callback.data.split(":")[1]))
            )

async def select_date(callback: CallbackQuery, callback_data: SelectDate, bot: Bot, state: FSMContext) -> None:
    if callback.message:
        await state.update_data({"week": callback_data.week, "strdate": callback_data.strdate})
        await callback.message.edit_text(text="Надрукуй інформацію:")
        await state.set_state(AddEventInfoStates.text)


async def event_info_text_input(message: Message, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    week: int = data.get("week") # type: ignore[assignment]
    event: CertainEvent = data.get("certain_event") # type: ignore[assignment]
    if message.from_user:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
        if message.content_type == ContentType.TEXT and message.text:
            verify_event = VerifyEvent(
                week=week,
                event_info=message.text
                )
            await message.answer(
                text= await VERIFY_EVENT_INFO.render_async(discipline_type=event.discipline_type, event_name=event.name, date=data.get("strdate"), info=message.text),
                reply_markup=get_approve())
            await state.update_data({"verify_event": verify_event})
        else:
            await message.reply("Це не текст!")
            await state.set_state(AddEventInfoStates.text)


async def add_event_info(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message and callback.data == "APPROVE":
        data = await state.get_data()
        user: Student = data.get("user") # type: ignore[assignment]
        verify_event: VerifyEvent = data.get("verify_event") # type: ignore[assignment]
        event_id: Union[UUID|str] = data.get("event_id") # type: ignore[assignment]
        await callback.message.edit_reply_markup()
        async with ScheduleAPI() as schedule_api:
            await schedule_api.add_event_info(event_id=event_id, group_id=user.group.id, verify_event=verify_event)
        await callback.message.answer("⬆️ Додано ⬆️")
        await state.clear()
    elif callback.message:
        await callback.message.delete()
        await state.clear()
    else:
        await state.clear()

