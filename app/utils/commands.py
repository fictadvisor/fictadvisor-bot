from typing import List, Tuple

from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScope,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeDefault,
)


async def set_bot_commands(bot: Bot) -> None:
    schedule = [
                BotCommand(command="today", description="Вивести розклад на сьогодні"),
                BotCommand(command="tomorrow", description="Вивести розклад на завтра"),
                BotCommand(command="week", description="Вивести розклад на тиждень"),
                BotCommand(command="next_week", description="Вивести розклад на наступний тиждень"),
                BotCommand(command="fortnight", description="Вивести на два тижні"),
                BotCommand(command="now", description="Вивести яка зараз пара"),
                BotCommand(command="left", description="Вивести скільки залишилось до кінця пари"),
                BotCommand(command="next", description="Вивести наступну пару"),
                BotCommand(command="add_info", description="Додати додаткову інформацію на пару"),
                BotCommand(command="enable", description="Включити/Виключити сповіщення")
            ]
    captain = [
                BotCommand(command="bind", description="Прив'язати тред для сповіщень"),
                BotCommand(command="start", description="Прив'язати телеграм групу"),
            ]
    uk_commands: Tuple[Tuple[List[BotCommand], BotCommandScope]] = (  # type: ignore[assignment]
        (
            schedule,
            BotCommandScopeDefault(),
        ),
        (
            schedule + captain,
            BotCommandScopeAllChatAdministrators(),
        ),
    )
    for commands, scope in uk_commands:
        await bot.set_my_commands(commands=commands, scope=scope)  # type: ignore[arg-type]
