import logging
from typing import Optional

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.api.schemas.message import Message
from app.api.stubs import BotStub
from app.settings import settings

broadcast_router = APIRouter(prefix="/broadcast", tags=["Broadcast"])


@broadcast_router.post('/sendMessage')
async def send_message_handler(
        message: Message,
        parse_mode: Optional[ParseMode] = None,
        chat_id: int = Query(default=settings.CHAT_ID, alias="id"),
        bot: Bot = Depends(BotStub)
) -> JSONResponse:
    logging.error(message.text)
    await bot.send_message(chat_id=chat_id, text=message.text, parse_mode=parse_mode)
    return JSONResponse(status_code=200, content={})
