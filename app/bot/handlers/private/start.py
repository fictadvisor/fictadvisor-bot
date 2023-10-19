from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.messages.private import REGISTER, START
from app.services.auth_api import AuthAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.telegram import RegisterTelegram
from app.services.user_api import UserAPI
from app.settings import settings
from app.utils.cache import cache


async def start(message: Message) -> None:
    await message.answer(await START.render_async(front_url=settings.FRONT_BASE_URL))
    try:
        async with UserAPI() as user_api:
            await user_api.get_user_by_telegram_id(message.chat.id)
    except ResponseException:
        async with AuthAPI() as api:
            await api.register_telegram(
                RegisterTelegram(
                    token=cache[message.from_user.id],  # type: ignore[union-attr]
                    telegram_id=message.from_user.id  # type: ignore[union-attr]
                )
            )
        url = f"{settings.FRONT_BASE_URL}/?token={cache[message.from_user.id]}"  # type: ignore[union-attr]
        await message.answer(
           text=await REGISTER.render_async(register_url=url),
           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Зареєструватись", url=url)]])
        )
