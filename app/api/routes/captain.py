from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.schemas.captain import BroadcastCaptain
from app.api.stubs import BotStub
from app.bot.schemas.captain import CaptainData
from app.messages.captain import BROADCAST_CAPTAIN
from app.services.user_api import State
from app.settings import settings
from app.utils import telegram

captain_router = APIRouter(prefix="/captains", tags=["Captains"])


@captain_router.post("/broadcastPending")
async def broadcast_captain(captain: BroadcastCaptain, bot: Bot = Depends(BotStub)):
    user = await telegram.get_user_by_id(bot, captain.telegram_id)

    await bot.send_message(
        chat_id=settings.CHAT_ID,
        text=await BROADCAST_CAPTAIN.render_async(data=captain, user=user),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Схвалити",
                                  callback_data=CaptainData(method=State.APPROVED,
                                                            user_id=captain.id,
                                                            telegram_id=captain.telegram_id).pack()),
             InlineKeyboardButton(text="Відмовити",
                                  callback_data=CaptainData(method=State.DECLINED,
                                                            user_id=captain.id,
                                                            telegram_id=captain.telegram_id).pack())]
        ])
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Successfully sent"
        }
    )
