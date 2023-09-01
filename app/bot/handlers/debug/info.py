from aiogram.types import Message


async def info(message: Message) -> None:
    await message.answer(f"User ID: <pre>{message.from_user.id}</pre>\nChat ID: <pre>{message.chat.id}</pre>")  # type: ignore[union-attr]
