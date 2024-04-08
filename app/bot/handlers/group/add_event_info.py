from contextlib import suppress
from typing import List, Optional
from app.services.exceptions.response_exception import ResponseException
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
from app.services.types.general_event import VerifyEvent
from app.services.types.general_events import FortnightGeneralEvents, GeneralEvent
from app.services.types.student import Student
from app.utils.events import what_week_event
from app.utils.discipline_type import get_discipline_type_color
from app.services.types.telegram_groups import TelegramGroupsByTelegramId, TelegramGroupByTelegramIdResponse
from app.services.telegram_group_api import TelegramGroup


async def add_info_command(message: Message, user: Student, state: FSMContext, telegram_groups: TelegramGroupsByTelegramId) -> None:
    await state.clear()

    async with ScheduleAPI() as schedule_api:
        fortnight_general_events = await schedule_api.get_general_group_events_by_fortnight(telegram_groups.telegram_groups[0].group.id)

    if not (fortnight_general_events.first_week_events or fortnight_general_events.second_week_events):
        await message.answer("На найближчий час пар немає")
        return

    all_group_events = fortnight_general_events.first_week_events + \
        fortnight_general_events.second_week_events
    all_unique_group_events = sorted(set(all_group_events))

    await state.update_data({
        "user": user,
        "fortnight_general_events": fortnight_general_events,
        "all_unique_group_events": all_unique_group_events,
        "telegram_group": telegram_groups.telegram_groups[0],
        "chat_id": message.chat.id
    })

    await message.answer(
        text="Вибери пару на яку хочеш додати інформацію\n\n🔵 Лекція 🟠 Практика 🟢 Лаба 🟣 Консультація",
        reply_markup=get_events_keyboard(all_unique_group_events)
    )
    await message.answer(
        text="Фільтрувати по:",
        reply_markup=get_events_filter_keyboard()
    )


async def filter_event(callback: CallbackQuery, callback_data: EventFilter, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    all_unique_group_events: List[GeneralEvent] = data.get(
        "all_unique_group_events")

    with suppress(TelegramBadRequest):
        await bot.edit_message_reply_markup(
            data.get("chat_id"), callback.message.message_id - 1,
            reply_markup=get_events_keyboard(
                all_unique_group_events, callback_data.type
            )
        )
    await callback.answer()


async def cancel(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if callback.data == "event_cancel":
        for i in range(2):
            await bot.delete_message(data.get("chat_id"), callback.message.message_id + i)
    elif callback.data == "date_cancel":
        await callback.message.delete()
    await callback.message.answer("Відміняю 🚫")
    await state.clear()


async def select_event(callback: CallbackQuery, callback_data: SelectEvent, bot: Bot, state: FSMContext) -> None:
    await state.update_data({"event_id": callback_data.event_id})
    data = await state.get_data()
    telegram_group: TelegramGroupByTelegramIdResponse = data.get(
        "telegram_group")
    fortnight_general_events: FortnightGeneralEvents = data.get(
        "fortnight_general_events")

    week = what_week_event(fortnight_general_events, callback_data.event_id)
    async with ScheduleAPI() as schedule_api:
        certain_event: CertainEvent = await schedule_api.get_certain_event(callback_data.event_id, telegram_group.group.id, week=week)

    await state.update_data({"certain_event": certain_event})

    await callback.message.delete()

    await bot.edit_message_text(
        text=f"{get_discipline_type_color(certain_event.discipline_type)} {certain_event.name}\nНа коли хочете додати інформацію?\nНайближчі пари в порядку зростання:",
        chat_id=data.get("chat_id"),
        message_id=callback.message.message_id + 1,
        reply_markup=get_events_dates(event=certain_event, week=week)
    )
    await callback.answer()


async def refresh_dates(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    certain_event: CertainEvent = data.get("certain_event")
    await callback.message.edit_reply_markup(
        reply_markup=get_events_dates(
            certain_event, week=int(callback.data.split(":")[1]))
    )


async def select_date(callback: CallbackQuery, callback_data: SelectDate, state: FSMContext) -> None:
    await state.update_data({"week": callback_data.week, "strdate": callback_data.strdate})
    await callback.message.edit_text(text="Надрукуй інформацію:")
    await state.set_state(AddEventInfoStates.text)


async def event_info_text_input(message: Message, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    week = data.get("week")
    event: CertainEvent = data.get("certain_event")
    await bot.delete_message(chat_id=data.get("chat_id"), message_id=message.message_id-1)
    if message.content_type == ContentType.TEXT:
        verify_event = VerifyEvent(
            week=week,
            eventInfo=message.text
        )
        await message.answer(
            text=await VERIFY_EVENT_INFO.render_async(
                discipline_type=event.discipline_type,
                event_name=event.name,
                date=data.get("strdate"),
                info=message.text
            ),
            reply_markup=get_approve()
        )
        await state.update_data({"verify_event": verify_event})
    else:
        await message.reply("Це не текст!\nНадрукуй інформацію ще раз:")
        await state.set_state(AddEventInfoStates.text)


async def add_event_info(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == "APPROVE":
        data = await state.get_data()
        telegram_group: TelegramGroupByTelegramIdResponse = data.get(
            "telegram_group")
        verify_event: VerifyEvent = data.get("verify_event")
        await callback.message.edit_reply_markup()
        try:
            async with ScheduleAPI() as schedule_api:
                await schedule_api.add_event_info(event_id=data.get("event_id"), group_id=telegram_group.group.id, verify_event=verify_event)
            await callback.message.answer("<b>API Call success</b>") # Debug
            await callback.message.answer("⬆️ Додано ⬆️")
        except ResponseException as ex:
            await callback.message.answer(f"<b>API Call failure: {ex.message}</b>") # Debug
            await callback.message.answer(f"{data.get('event_id')}") # Debug
        await state.clear()
    else:
        await callback.message.delete()
        await state.clear()
