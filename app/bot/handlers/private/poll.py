import logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import ScenesManager
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.poll_keyboard import (
    get_users_teachers_keyboard,
)
from app.bot.keyboards.types.select_teacher import SelectTeacher
from app.bot.scenes.poll import PollScene
from app.services.exceptions.response_exception import ResponseException
from app.services.poll_api import PollAPI
from app.services.types.student import Student
from app.services.types.users_teachers import UsersTeachers
from app.services.user_api import UserAPI
from app.utils.telegram import send_answer


async def poll_command(message: Message, state: FSMContext) -> None:
    try:
        async with UserAPI() as user_api:
            user: Student = await user_api.get_user_by_telegram_id(message.from_user.id)  #type: ignore[union-attr]
            await state.update_data({"user": user})
    except ResponseException as e:
        await send_answer(message, "Прив'яжіть телеграм до аккаунта FICE Advisor")
        logging.error(e)
        return

    async with PollAPI() as poll_api:
        users_teachers: UsersTeachers = await poll_api.get_users_teachers(user_id=user.id)

    await message.answer(
        "Вибери викладача:",
        reply_markup=get_users_teachers_keyboard(users_teachers)
    )

async def select_teacher(callback: CallbackQuery, callback_data: SelectTeacher, scenes: ScenesManager) -> None:
    if callback.message and hasattr(callback.message, 'answer') and hasattr(callback.message, 'delete'):
        await callback.message.delete()
        await scenes.enter(PollScene, discipline_teacher_id=callback_data.discipline_teacher_id)
        await callback.answer()
