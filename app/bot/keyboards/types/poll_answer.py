from typing import Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class PollAnswer(CallbackData, prefix="answer_poll"):
    question_id: Union[str, UUID]
    value: str


class SubmitPoll(CallbackData, prefix="submit_poll"):
    pass


class CancelPoll(CallbackData, prefix="cancel_poll"):
    pass


class BackPoll(CallbackData, prefix="back_poll"):
    pass
