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
from app.bot.handlers.group.add_event_info import (
    add_event_info,
    add_info_command,
    cancel,
    event_info_text_input,
    filter_event,
    select_date,
    select_event,
)
from app.bot.handlers.group.bind import bind
from app.bot.handlers.group.captain_button_press_callback import (
    captain_button_press_callback,
)
from app.bot.handlers.group.enable import enable
from app.bot.handlers.group.fortnight import fortnight, select_week
from app.bot.handlers.group.invite_bot import invite_bot, migrate_chat
from app.bot.handlers.group.kick_bot import kick_bot
from app.bot.handlers.group.left import left_command
from app.bot.handlers.group.next import next_command
from app.bot.handlers.group.now import now_command
from app.bot.handlers.group.today import today
from app.bot.handlers.group.tomorrow import tomorrow
from app.bot.handlers.group.week import week
from app.bot.keyboards.types.event_info import (
    EventApprove,
    EventCancel,
    EventEdit,
    EventFilter,
    SelectDate,
    SelectEvent,
)
from app.bot.keyboards.types.select_week import SelectWeek
from app.bot.states.event_info_states import AddEventInfoStates

router = Router(name=__name__)
router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

router.my_chat_member.register(kick_bot, ChatMemberUpdatedFilter(LEAVE_TRANSITION))

router.my_chat_member.register(invite_bot, ChatMemberUpdatedFilter(JOIN_TRANSITION))
router.message.register(invite_bot, CommandStart(), IsCaptainOrDeputy())
router.message.register(migrate_chat, F.migrate_from_chat_id.as_("migrate_from_chat_id"))

router.callback_query.register(captain_button_press_callback, F.data == "captain_press", IsCaptainOrDeputy())

router.message.register(bind, Command("bind"), F.reply_to_message.forum_topic_created, ChatBound(), IsCaptainOrDeputy())
router.message.register(enable, Command("enable"), ChatBound(), IsCaptainOrDeputy())

router.message.register(today, Command("today"), ChatBound())
router.message.register(tomorrow, Command("tomorrow"), ChatBound())
router.message.register(week, Command("week"), ChatBound())
router.message.register(fortnight, Command("fortnight"), ChatBound())
router.message.register(now_command, Command("now"), ChatBound())
router.message.register(left_command, Command("left"), ChatBound())
router.message.register(next_command, Command("next"), ChatBound())
router.message.register(add_info_command, Command("add_info"), ChatBound(), IsCaptainOrDeputy())
router.message.register(event_info_text_input, AddEventInfoStates.text)
router.callback_query.register(add_event_info, EventApprove.filter(), IsCaptainOrDeputy())
router.callback_query.register(add_event_info, EventEdit.filter(), IsCaptainOrDeputy())
router.callback_query.register(cancel, EventCancel.filter(), IsCaptainOrDeputy())
router.callback_query.register(select_week, SelectWeek.filter(), IsCaptainOrDeputy())
router.callback_query.register(select_event, SelectEvent.filter(), IsCaptainOrDeputy())
router.callback_query.register(filter_event, EventFilter.filter(), IsCaptainOrDeputy())
router.callback_query.register(select_date, SelectDate.filter(), IsCaptainOrDeputy())

router.callback_query.register(select_week, SelectWeek.filter())
