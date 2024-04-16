
from typing import List

from aiogram import Bot
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, ContentType, Message

from app.bot.keyboards.poll_keyboard import get_poll_keyboard, get_submit_edit_keyboard
from app.bot.keyboards.types.poll_answer import (
    BackPoll,
    CancelPoll,
    PollAnswer,
    SubmitPoll,
)
from app.bot.keyboards.types.select_teacher import SelectTeacher
from app.messages.poll import POLL_QUESTION, SUBMIT_MSG
from app.services.response_api import ResponseAPI
from app.services.types.answer import Answer
from app.services.types.question import Question
from app.services.types.response import UsersAnswers, UsersQuestions
from app.services.types.student import Student


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
        if callback.message:
            await self.wizard.state.update_data(
                {
                    "discipline_teacher_id": discipline_teacher_id,
                    "questions": questions,
                    "answers": [],
                    "question_step": question_step,
                    "message_id": callback.message.message_id + 1
                }
            )

        if callback.message and hasattr(callback.message, 'answer'):
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
        if callback.message and hasattr(callback.message, 'edit_text'):
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
    async def cancel(self, callback: CallbackQuery) -> None:
        await callback.answer(
            "Ви скасували опитування!"
        )
        if callback.message and hasattr(callback.message, 'delete'):
            await callback.message.delete()
        await self.wizard.state.clear()

    @on.callback_query(BackPoll.filter())
    async def prev(self, callback: CallbackQuery) -> None:
        data = await self.wizard.state.get_data()
        questions = data.get("questions")
        question_step = data.get("question_step", 0)
        answers: List[Answer] = data.get("answers", [])
        answers.pop()
        await self.wizard.state.update_data({"answers": answers})
        if question_step - 1 < 0:
            return await self.wizard.exit()
        await self.wizard.state.update_data({"question_step": question_step - 1})
        if questions:
            return await self.question(
                callback=callback,
                questions=questions,
                question_step=question_step - 1
            )
        else:
            pass

    @on.callback_query(PollAnswer.filter())
    async def next(self, callback: CallbackQuery, callback_data: PollAnswer) -> None:
        if callback.message and hasattr(callback.message, 'answer') and hasattr(callback.message, 'delete') and hasattr(callback.message, 'edit_text'):
            await callback.answer()

            data = await self.wizard.state.get_data()
            questions: List[Question] = data.get("questions")  # type: ignore[assignment]
            question_step: int = data.get("question_step")  # type: ignore[assignment]
            answers: List[Answer] = data.get("answers", [])
            answers.append(
                Answer(
                    question_id=callback_data.question_id,
                    value=callback_data.value
                )
            )
            if question_step:
                await self.wizard.state.update_data(
                    {
                        "answers": answers,
                        "question_step": question_step + 1,
                        "question_id": callback_data.question_id
                    }
                )
            if question_step + 1 >= len(questions):
                if callback.message and hasattr(callback.message, 'edit_text'):
                    await callback.message.edit_text(
                        await SUBMIT_MSG.render_async(
                            questions=questions,
                            answers=answers
                        ),
                        reply_markup=get_submit_edit_keyboard()
                    )
            else:
                await self.question(
                    callback=callback,
                    questions=questions,
                    question_step=question_step + 1
                )

    @on.message()
    async def poll_comment(self, message: Message, bot: Bot) -> None:
        data = await self.wizard.state.get_data()
        questions: List[Question] = data.get("questions")  # type: ignore[assignment]
        question_step: int = data.get("question_step") # type: ignore[assignment]
        if question_step == len(questions) - 1:
            await self.wizard.state.update_data({"question_step": question_step + 1})
            if message.content_type == ContentType.TEXT and message.text:
                answers: List[Answer] = data.get("answers") # type: ignore[assignment]
                answers.append(
                    Answer(
                        question_id=questions[question_step].id,
                        value=message.text
                    )
                )
                await bot.edit_message_text(
                    await SUBMIT_MSG.render_async(
                        questions=questions,
                        answers=answers
                    ),
                    chat_id=message.chat.id,
                    message_id=data.get("message_id"),
                    reply_markup=get_submit_edit_keyboard()
                )
        else:
            await message.answer("Письмова відповідь буде в кінці.")

    @on.callback_query(SubmitPoll.filter())
    async def submit(self, callback: CallbackQuery) -> None:
        if callback.message and hasattr(callback.message, 'answer') and hasattr(callback.message, 'delete') and hasattr(callback.message, 'edit_text'):
            data = await self.wizard.state.get_data()
            discipline_teacher_id: str = data.get('discipline_teacher_id')  # type: ignore[assignment]
            await callback.message.answer(text=str(discipline_teacher_id))
            answers: List[Answer] = data.get('answers')  # type: ignore[assignment]
            await callback.message.answer(text=str(answers))
            user: Student = data.get('user')  # type: ignore[assignment]
            async with ResponseAPI() as response_api:
                await response_api.post_users_answers(
                    discipline_teacher_id=discipline_teacher_id,
                    user_answers=UsersAnswers(
                        answers=answers,
                        user_id=user.id
                    )
                )
            await callback.message.answer("Відповіді надіслано!")
            await callback.message.delete()
            await self.wizard.state.clear()
        return await self.wizard.exit()
