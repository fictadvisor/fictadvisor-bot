from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery

from app.bot.keyboards.poll_keyboard import get_poll_keyboard
from app.bot.keyboards.types.poll_answer import (
    BackPoll,
    CancelPoll,
    PollAnswer,
    SubmitPoll,
)
from app.bot.keyboards.types.select_teacher import SelectTeacher
from app.messages.poll import POLL_QUESTION
from app.services.response_api import ResponseAPI
from app.services.types.answer import Answer
from app.services.types.response import UsersQuestions
from app.services.types.student import Student


class PollScene(Scene, state="poll"):

    @on.callback_query.enter(SelectTeacher.filter())
    async def on_enter(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        discipline_teacher_id: str,
        category_step: int = 0,
        question_step: int = 0
    ) -> None:
        data = await state.get_data()
        user: Student = data.get("user") # type: ignore[assignment]
        async with ResponseAPI() as response_api:
            users_questions: UsersQuestions = await response_api.get_users_questions(discipline_teacher_id, user.id)

        if data.get("discipline_teacher_id"):
            if callback.message:
                await callback.message.edit_text(
                    await POLL_QUESTION.render_async(
                        category=users_questions.categories[category_step].name,
                        name=users_questions.categories[category_step].questions[question_step].name,
                        description=users_questions.categories[category_step].questions[question_step].description,
                        criteria=users_questions.categories[category_step].questions[question_step].criteria
                    ),
                    reply_markup=get_poll_keyboard(
                        question_id=users_questions.categories[category_step].questions[question_step].id,
                        question_step=question_step,
                        category_step=category_step,
                        question_type=users_questions.categories[category_step].questions[question_step].type
                    )
                )
        else:
            if callback.message:
                await callback.message.answer(
                    await POLL_QUESTION.render_async(
                        category=users_questions.categories[category_step].name,
                        name=users_questions.categories[category_step].questions[question_step].name,
                        description=users_questions.categories[category_step].questions[question_step].description,
                        criteria=users_questions.categories[category_step].questions[question_step].criteria
                    ),
                    reply_markup=get_poll_keyboard(
                        question_id=users_questions.categories[category_step].questions[question_step].id,
                        question_step=question_step,
                        category_step=category_step,
                        question_type=users_questions.categories[category_step].questions[question_step].type
                    )
                )
        await state.update_data(
            {
                "discipline_teacher_id": discipline_teacher_id,
                "category_step": category_step,
                "question_step": question_step,
                "len_of_categories": len(users_questions.categories),
                "len_of_questions": len(users_questions.categories[category_step].questions)
            }
        )

    @on.callback_query(CancelPoll.filter())
    async def cancel(self, callback: CallbackQuery):
        await callback.message.delete()
        await self.wizard.state.clear()

    @on.callback_query(BackPoll.filter())
    async def prev(self, callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        category_step = data.get("category_step")
        question_step = data.get("question_step")
        len_of_questions = data.get("len_of_questions")
        discipline_teacher_id = data.get("discipline_teacher_id")

        if question_step - 1 < 0:
            if category_step - 1 < 0:
                return await self.wizard.exit()
            return await self.wizard.retake(
                discipline_teacher_id=discipline_teacher_id,
                category_step=category_step - 1,
                question_step=len_of_questions - 1
            )
        return await self.wizard.retake(
            discipline_teacher_id=discipline_teacher_id,
            category_step=category_step,
            question_step=question_step - 1
        )

    @on.callback_query(PollAnswer.filter())
    async def poll_answer(self, callback: CallbackQuery, callback_data: PollAnswer, state: FSMContext):
        await state.update_data(
            {
                "answers": [
                    Answer(
                        questionId=callback_data.question_id,
                        value=callback_data.value
                    )
                ]
            }
        )
        await callback.answer()

        data = await state.get_data()
        category_step = data.get("category_step")
        question_step = data.get("question_step")
        len_of_categories = data.get("len_of_categories")
        len_of_questions = data.get("len_of_questions")
        discipline_teacher_id = data.get("discipline_teacher_id")

        new_question_step = question_step + 1
        if new_question_step >= len_of_questions:
            if category_step + 1 >= len_of_categories:
                return await self.wizard.exit()
            category_step += 1
            new_question_step = 0
        return await self.wizard.retake(
            discipline_teacher_id=discipline_teacher_id,
            question_step=new_question_step,
            category_step=category_step
        )

    @on.callback_query(SubmitPoll.filter())
    async def submit(self, callback: CallbackQuery, state: FSMContext):
        await state.get_data()
        # try:
        #     async with ResponseAPI() as response_api:
        #         await response_api.post_users_answers(
        #             discipline_teacher_id=data.get('discipline_teacher_id'),
        #             user_answers=UsersAnswers(
        #                 answers=data.get('answers'),
        #                 user_id=data.get('user_id')
        #             )
        #         )
        # except ResponseException as ex:
        #     await callback.message.answer(
        #         f"API FAILURE: {ex.message}"
        #     )
        await callback.message.answer("API Call")
        return await self.wizard.exit()
