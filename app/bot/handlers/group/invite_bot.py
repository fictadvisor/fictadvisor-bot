from aiogram import Bot
from aiogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup


async def invite_bot(event: ChatMemberUpdated, bot: Bot) -> None:
    await bot.send_message(
        chat_id=event.chat.id,
        text="Староста групи має натиснути цю кнопку",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Тиць", callback_data="captain_press")]]),
    )
