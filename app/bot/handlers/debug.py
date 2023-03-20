from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

debug_router = Router(name=__name__)


@debug_router.message(Command("debug"))
async def echo_handler(message: Message):
    await message.answer(f"User ID: <pre>{message.from_user.id}</pre>\nChat ID: <pre>{message.chat.id}</pre>")
