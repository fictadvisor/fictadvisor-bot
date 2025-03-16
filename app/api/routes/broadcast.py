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


@broadcast_router.post("/sendMessage")
async def send_message_handler(
    message: Message,
    parse_mode: Optional[ParseMode] = None,
    chat_id: int = Query(default=settings.CHAT_ID, alias="id"),
    bot: Bot = Depends(BotStub),
) -> JSONResponse:
    await bot.send_message(chat_id=chat_id, text=message.text, parse_mode=parse_mode)
    return JSONResponse(status_code=200, content={})


@broadcast_router.post("/error")
async def send_error_handler(
    message: Message,
    chat_id: int = Query(default=settings.ERRORS_CHAT_ID, alias="id"),
    thread_id: Optional[int] = Query(default=settings.ERRORS_THREAD_ID, alias="thread"),
    bot: Bot = Depends(BotStub),
) -> JSONResponse:
    logging.error(message.text)

    text_splitted = message.text.split("\n")

    error_messages: list[str] = []
    traceback: list[str] = []
    is_error_text = True

    for line in text_splitted:
        if not line:
            continue

        if is_error_text:
            if not line.startswith("  "):
                error_messages.append(f"<code>{line}</code>")
                continue

            is_error_text = False

        traceback.append(line)

    traceback_filtered: list[str] = []
    for line in traceback:
        if not line.startswith("  "):
            traceback_filtered.append(line)
            continue

        src_index = line.find("/src/")
        if src_index == -1:
            continue

        bracket_index = line.rfind("(", 0, src_index)
        if bracket_index == -1:
            continue

        line_formatted = line[: bracket_index + 1].lstrip() + line[src_index + 1 :]
        traceback_filtered.append(line_formatted)

    error_message = "\n".join(error_messages)
    traceback_message = ""
    if len(traceback_filtered):
        traceback_message = (
            "\n\n<pre>Traceback:\n" + "\n".join(traceback_filtered) + "</pre>"
        )

    error_text = "🚨 <b>Backend Error</b> 🚨\n\n" + error_message + traceback_message
    await bot.send_message(
        chat_id=chat_id,
        message_thread_id=thread_id,
        text=error_text,
        parse_mode="HTML",
    )

    return JSONResponse(status_code=200, content={})
