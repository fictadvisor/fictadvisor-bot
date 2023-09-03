from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.schemas.superhero import BroadcastSuperhero
from app.api.stubs import BotStub
from app.bot.schemas.superhero import SuperheroData
from app.enums.state import State
from app.messages.superhero import BROADCAST_SUPERHERO
from app.settings import settings
from app.utils import telegram

superhero_router = APIRouter(prefix="/superheroes", tags=["Superheroes"])


@superhero_router.post("/broadcastPending")
async def broadcast_superhero(student: BroadcastSuperhero, bot: Bot = Depends(BotStub)) -> JSONResponse:
    user = await telegram.get_user_by_id(bot, student.telegram_id)
    await bot.send_message(
        chat_id=settings.CHAT_ID,
        text=await BROADCAST_SUPERHERO.render_async(data=student, user=user),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Схвалити",
                                  callback_data=SuperheroData(method=State.APPROVED,
                                                              user_id=student.id,
                                                              telegram_id=student.telegram_id).pack()),
             InlineKeyboardButton(text="Відмовити",
                                  callback_data=SuperheroData(method=State.DECLINED,
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
