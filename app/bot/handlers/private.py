from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.messages.private import START, REGISTER
from app.services.auth_api import AuthAPI
from app.settings import settings
from app.utils.cache import AuthCache

private_router = Router(name=__name__)
private_router.message.filter(F.chat.type == ChatType.PRIVATE)

cache = AuthCache(maxsize=1000, ttl=60*60)


@private_router.message(Command("start"))
async def start(message: Message):
    async with AuthAPI() as api:
        await api.register_telegram(
            token=cache[message.from_user.id],
            telegram_id=message.from_user.id
        )
    url = f"{settings.FRONT_BASE_URL}/?token={cache[message.from_user.id]}"

    await message.answer(await START.render_async(front_url=settings.FRONT_BASE_URL))
    await message.answer(
       text=await REGISTER.render_async(register_url=url),
       reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Зареєструватись", url=url)]])
    )
