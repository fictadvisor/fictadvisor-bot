from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.schemas.response import BroadcastResponse
from app.api.stubs import BotStub
from app.bot.schemas.response import ResponseData
from app.messages.response import BROADCAST_RESPONSE
from app.services.user_api import UserAPI, State
from app.settings import settings

response_router = APIRouter(prefix="/responses", tags=["Responses"])


@response_router.post("/broadcastPending")
async def broadcast_response(
        response: BroadcastResponse,
        bot: Bot = Depends(BotStub)
):
    async with UserAPI() as api:
        user = await api.get_user(response.user_id)
        if user.get("firstName") is not None:
            await bot.send_message(
                chat_id=settings.CHAT_ID,
                text=await BROADCAST_RESPONSE.render_async(data=response, user=user),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Схвалити", callback_data=ResponseData(method=State.APPROVED,
                                                                                      discipline_teacher_id=response.discipline_teacher_id).pack()),
                     InlineKeyboardButton(text="Відмовити", callback_data=ResponseData(method=State.DECLINED,
                                                                                       discipline_teacher_id=response.discipline_teacher_id).pack())]
                ])
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Successfully sent"
                }
            )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "User not found"
        }
    )
