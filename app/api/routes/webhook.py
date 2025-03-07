from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import SecretStr
from starlette import status

from app.api.stubs import BotStub, DispatcherStub, SecretStub

webhook_router = APIRouter(prefix="/webhook", tags=["Telegram Webhook"])


@webhook_router.post("")
async def webhook_route(
    request: Request,
    update: Update,
    secret: SecretStr = Header(alias="X-Telegram-Bot-Api-Secret-Token"),
    expected_secret: str = Depends(SecretStub),
    bot: Bot = Depends(BotStub),
    dispatcher: Dispatcher = Depends(DispatcherStub),
) -> JSONResponse:
    if secret.get_secret_value() != expected_secret:
        raise HTTPException(
            detail="Invalid secret", status_code=status.HTTP_401_UNAUTHORIZED
        )

    message = update.message
    if message:
        message_info: dict[str, str] = {"chat_id": str(message.chat.id)}
        user = message.from_user
        if user:
            message_info["user_id"] = str(user.id)
            message_info["full_name"] = user.full_name

            if user.username:
                message_info["username"] = user.username

        request.state.message_info = message_info

    await dispatcher.feed_update(bot, update=update)

    return JSONResponse(status_code=200, content={"ok": True})
