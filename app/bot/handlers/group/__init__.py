from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import (
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
    ChatMemberUpdatedFilter,
    CommandStart,
)

from app.bot.handlers.group.captain_button_press_callback import (
    captain_button_press_callback,
)
from app.bot.handlers.group.invite_bot import invite_bot, migrate_chat
from app.bot.handlers.group.kick_bot import kick_bot

router = Router(name=__name__)
router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

router.my_chat_member.register(kick_bot, ChatMemberUpdatedFilter(LEAVE_TRANSITION))

router.my_chat_member.register(invite_bot, ChatMemberUpdatedFilter(JOIN_TRANSITION))
router.message.register(invite_bot, CommandStart())
router.message.register(migrate_chat, F.migrate_from_chat_id.as_("migrate_from_chat_id"))

router.callback_query.register(captain_button_press_callback, F.data == "captain_press")
