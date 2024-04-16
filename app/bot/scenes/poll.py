from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery

from app.bot.keyboards.poll_keyboard import get_poll_keyboard, get_edit_questions_keyboard, get_submit_edit_keyboard
from app.bot.keyboards.types.poll_answer import (
    BackPoll,
    CancelPoll,
    PollAnswer,
    SubmitPoll,
    EditPoll
)
from app.bot.keyboards.types.select_teacher import SelectTeacher
from app.messages.poll import POLL_QUESTION, SUBMIT_MSG
from app.services.response_api import ResponseAPI
from app.services.types.answer import Answer
from app.services.types.response import UsersQuestions
from app.services.types.student import Student
from typing import List
from app.services.types.question import Question


class PollScene(Scene, state="poll"):

    @on.callback_query.enter(SelectTeacher.filter())
    async def on_enter(
        self,
        callback: CallbackQuery,
        discipline_teacher_id: str,
        question_step: int = 0
    ) -> None:
        data = await self.wizard.state.get_data()
        user: Student = data.get("user")  # type: ignore[assignment]
        async with ResponseAPI() as response_api:
            users_questions: UsersQuestions = await response_api.get_users_questions(discipline_teacher_id, user.id)
            questions: List[Question] = []
            for category in users_questions.categories:
                questions.extend(category.questions)
        await self.wizard.state.update_data({"questions": questions, "answers": [], "question_step": question_step})

        if callback.message:
            await callback.message.answer(
                await POLL_QUESTION.render_async(
                    question=questions[question_step]
                ),
                reply_markup=get_poll_keyboard(
                    question=questions[question_step],
                    question_step=question_step,
                )
            )

    async def question(
        self,
        callback: CallbackQuery,
        questions: List[Question],
        question_step: int
    ) -> None:
        if callback.message:
            await callback.message.edit_text(
                await POLL_QUESTION.render_async(
                    question=questions[question_step]
                ),
                reply_markup=get_poll_keyboard(
                    question=questions[question_step],
                    question_step=question_step,
                )
            )

    @on.callback_query(CancelPoll.filter())
    async def cancel(self, callback: CallbackQuery):
        await callback.answer(
            "Ви скасували опитування!"
        )
        await callback.message.delete()
        await self.wizard.state.clear()

    @on.callback_query(BackPoll.filter())
    async def prev(self, callback: CallbackQuery):
        data = await self.wizard.state.get_data()
        questions = data.get("questions")
        question_step = data.get("question_step")
        answers: list = data.get("answers")
        answers.pop()
        await self.wizard.state.update_data({"answers": answers})
        if question_step - 1 < 0:
            return await self.wizard.exit()
        await self.wizard.state.update_data({"question_step": question_step - 1})
        return await self.question(
            callback=callback,
            questions=questions,
            question_step=question_step - 1
        )

    @on.callback_query(PollAnswer.filter())
    async def next(self, callback: CallbackQuery, callback_data: PollAnswer):
        await callback.answer()

        data = await self.wizard.state.get_data()
        questions = data.get("questions")
        question_step = data.get("question_step")
        answers: list = data.get("answers")
        answers.append(
            Answer(
                question_id=callback_data.question_id,
                value=callback_data.value
            )
        )
        await self.wizard.state.update_data({"answers": answers})
        if question_step + 1 >= len(questions):
            return await callback.message.edit_text(
                await SUBMIT_MSG.render_async(
                    questions=questions,
                    answers=answers
                ),
                reply_markup=get_submit_edit_keyboard()
            )
        await self.wizard.state.update_data({"question_step": question_step + 1})
        return await self.question(
            callback=callback,
            questions=questions,
            question_step=question_step + 1
        )
    
    @on.callback_query(EditPoll.filter())
    async def edit(self, callback: CallbackQuery):
        questions = (await self.wizard.state.get_data()).get("questions")
        await callback.message.answer(
            "Обери відповідь яку хочеш змінити:",
            reply_markup=get_edit_questions_keyboard(questions=questions)
        )

    @on.callback_query(SubmitPoll.filter())
    async def submit(self, callback: CallbackQuery):
        # data = await self.wizard.state.get_data()
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
        await self.wizard.state.clear()
        return await self.wizard.exit()
    
    

        