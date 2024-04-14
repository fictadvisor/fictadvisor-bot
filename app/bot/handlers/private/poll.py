from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.user_api import UserAPI
from app.services.poll_api import PollAPI
from app.services.response_api import ResponseAPI
from app.services.types.student import Student
from app.services.types.users_teachers import UsersTeachers
from app.services.types.response import UsersQuestions
from app.bot.keyboards.teachers_keyboard import get_teachers_keyboard
from app.bot.keyboards.types.select_teacher import SelectTeacher
from aiogram.fsm.scene import ScenesManager
from app.bot.scenes.poll import PollScene


async def poll_command(message: Message, state: FSMContext):
    async with UserAPI() as user_api:
        user: Student = await user_api.get_user_by_telegram_id(message.from_user.id)
        await state.update_data({"user": user})
    async with PollAPI() as poll_api:
        users_teachers: UsersTeachers = await poll_api.get_users_teachers(user_id=user.id)

    await message.answer(
        "Вибери викладача:",
        reply_markup=get_teachers_keyboard(users_teachers)
    )

async def select_teacher(callback: CallbackQuery, callback_data: SelectTeacher, scenes: ScenesManager):
    await scenes.enter(PollScene, discipline_teacher_id=callback_data.discipline_teacher_id)
    await callback.answer()


