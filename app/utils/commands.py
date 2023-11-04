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
                BotCommand(command="fortnight", description="Вивести на два тижні")
            ]
    captain = [
                BotCommand(command="bind", description="Прив'язати тред для сповіщень"),
                BotCommand(command="enable", description="Включити/Виключити сповіщення"),
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
