from aiogram.fsm.scene import Scene, SceneRegistry, ScenesManager, on
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
from aiogram import F
from typing import Optional

class PollScene(Scene, state="poll"):

    @on.callback_query.enter()
    async def on_enter(self, callback: CallbackQuery, state: FSMContext, discipline_teacher_id: Optional[str] = None):
        data = await state.get_data()
        user: Student = data.get("user")
        print(user)
        async with ResponseAPI() as response_api:
            users_questions: UsersQuestions = await response_api.get_users_questions(discipline_teacher_id, user.id)
        await callback.message.answer(users_questions.categories[0].name)
        await callback.answer()