from aiogram.types import Message

from app.messages.general import HELP


async def help_command(message: Message) -> None:
    await message.reply(HELP)
