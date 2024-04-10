from aiogram.types import Message, CallbackQuery
from app.services.user_api import UserAPI
from app.services.poll_api import PollAPI
from app.services.types.student import Student
from app.services.types.users_teachers import UsersTeachers
from app.bot.keyboards.teachers_keyboard import get_teachers_keyboard
from app.bot.keyboards.types.select_teacher import SelectTeacher


async def poll_command(message: Message) -> None:
    async with UserAPI() as user_api:
        user: Student = await user_api.get_user_by_telegram_id(message.from_user.id)
    async with PollAPI() as poll_api:
        users_teachers: UsersTeachers = await poll_api.get_users_teachers(user_id=user.id)

    await message.answer(
        "Вибери викладача:",
        reply_markup=get_teachers_keyboard(users_teachers)
    )

async def teacher(callback: CallbackQuery, callback_data: SelectTeacher):
    await callback.message.answer(f"Pupupupu")
    await callback.answer()
