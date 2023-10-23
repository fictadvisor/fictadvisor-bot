from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import (
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
    ChatMemberUpdatedFilter,
    Command,
    CommandStart,
)

from app.bot.filters.chat_bound import ChatBound
from app.bot.filters.is_captain_or_deputy import IsCaptainOrDeputy
from app.bot.handlers.group.bind import bind
from app.bot.handlers.group.captain_button_press_callback import (
    captain_button_press_callback,
)
from app.bot.handlers.group.enable import enable
from app.bot.handlers.group.fortnight import fortnight, select_week
from app.bot.handlers.group.invite_bot import invite_bot, migrate_chat
from app.bot.handlers.group.kick_bot import kick_bot
from app.bot.handlers.group.today import today
from app.bot.handlers.group.tomorrow import tomorrow
from app.bot.handlers.group.week import week
from app.bot.keyboards.types.select_week import SelectWeek

router = Router(name=__name__)
router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

router.my_chat_member.register(kick_bot, ChatMemberUpdatedFilter(LEAVE_TRANSITION))

router.my_chat_member.register(invite_bot, ChatMemberUpdatedFilter(JOIN_TRANSITION))
router.message.register(invite_bot, CommandStart(), IsCaptainOrDeputy())
router.message.register(migrate_chat, F.migrate_from_chat_id.as_("migrate_from_chat_id"))

router.callback_query.register(captain_button_press_callback, F.data == "captain_press", IsCaptainOrDeputy())

router.message.register(bind, Command("bind"), F.reply_to_message.forum_topic_created, ChatBound(), IsCaptainOrDeputy())
router.message.register(enable, Command("enable"), ChatBound(), IsCaptainOrDeputy())

router.message.register(today, Command("today"))
router.message.register(tomorrow, Command("tomorrow"))
router.message.register(week, Command("week"))
router.message.register(fortnight, Command("fortnight"))
router.callback_query.register(select_week, SelectWeek.filter())
