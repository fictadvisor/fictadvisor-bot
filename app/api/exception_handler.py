import traceback

from aiogram import Bot
from aiogram.types import LinkPreviewOptions
from fastapi import Request
from fastapi.responses import JSONResponse

from app.settings import settings


async def exception_handler(request: Request, exc: Exception, bot: Bot) -> JSONResponse:
    tb = traceback.extract_tb(exc.__traceback__)
    filtered_tb = [line for line in tb if "app" in line.filename]
    filtered_tb_list = traceback.format_list(filtered_tb)
    formatted_tb: list[str] = []
    for line in filtered_tb_list:
        app_index = line.find("app")
        if app_index == -1:
            continue

        quoutation_index = line.rfind('"', 0, app_index)
        if quoutation_index == -1:
            continue

        line_formatted = line[: quoutation_index + 1].lstrip() + line[app_index:]
        formatted_tb.append(line_formatted)

    try:
        message_info: dict[str, str] = request.state.message_info
        chat_id = message_info.get("chat_id")
        user_id = message_info.get("user_id")
        full_name = message_info.get("full_name")
        username = message_info.get("username")

        footer = f"<code>{chat_id}</code>"
        if user_id:
            footer += f" | <code>{user_id}</code> | "

            if username:
                footer += f"<a href='https://t.me/{username}'>{full_name}</a>"
            else:
                footer += f"<code>{full_name}</code>"
    except AttributeError:
        footer = ""

    error_text = (
        "🚨 <b>Bot Error</b> 🚨\n\n<code>"
        + str(exc)
        + "</code>\n\n<pre>Traceback:\n"
        + "".join(formatted_tb)
        + "</pre>\n"
        + footer
    )

    await bot.send_message(
        chat_id=settings.ERRORS_CHAT_ID,
        message_thread_id=settings.ERRORS_THREAD_ID,
        text=error_text,
        parse_mode="HTML",
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )

    return JSONResponse(status_code=200, content={})
