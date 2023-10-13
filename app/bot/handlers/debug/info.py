from aiogram.types import Message

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.user_api import UserAPI


async def info(message: Message) -> None:

    async with UserAPI() as user_api:

        try:
            user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type:ignore[union-attr]
            await message.reply(f"Username: <pre>{user.username}</pre>")
        except ResponseException:
            await message.reply("Схоже, в вас немає акаунту на ФіктАдвізорі.")

    async with TelegramGroupAPI() as telegram_api:
        try:
            groups = [group.group.code for group in (await telegram_api.get_by_telegram_id(message.chat.id)).telegram_groups]  # type:ignore[union-attr]
            await message.reply(f"Групи прив'язані до даного чату: <pre>{', '.join(groups)}</pre>")
        except ResponseException:
            await message.reply("Схоже, груп на даний момент не закріплено.")
