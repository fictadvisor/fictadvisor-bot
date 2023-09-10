from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import LEAVE_TRANSITION, ChatMemberUpdatedFilter

from app.bot.handlers.group.kick_bot import kick_bot

router = Router(name=__name__)
router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

router.my_chat_member.register(kick_bot, ChatMemberUpdatedFilter(LEAVE_TRANSITION))
