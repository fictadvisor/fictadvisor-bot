from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.schemas.student import BroadcastStudent
from app.api.stubs import BotStub
from app.bot.schemas.student import StudentData
from app.messages.student import BROADCAST_STUDENT
from app.services.user_api import State
from app.utils import telegram

student_router = APIRouter(prefix="/students", tags=["Students"])


@student_router.post("/broadcastPending")
async def broadcast_student(student: BroadcastStudent, bot: Bot = Depends(BotStub)):
    user = await telegram.get_user_by_id(bot, student.telegram_id)
    try:
        await bot.send_message(
            chat_id=student.captain_telegram_id,
            text=await BROADCAST_STUDENT.render_async(data=student, user=user),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Схвалити",
                                      callback_data=StudentData(method=State.APPROVED,
                                                                user_id=student.id,
                                                                telegram_id=student.telegram_id).pack()),
                 InlineKeyboardButton(text="Відмовити",
                                      callback_data=StudentData(method=State.DECLINED,
                                                                user_id=student.id,
                                                                telegram_id=student.telegram_id).pack())]
            ])
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Successfully sent"
            }
        )

    except TelegramBadRequest:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Incorrect captain telegram id"
            }
        )
