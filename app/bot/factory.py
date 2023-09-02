from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.bot.handlers import router as main_router
from app.enums.telegram_source import TelegramSource
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.create_telegram_group import CreateTelegramGroup
from app.settings import settings


async def on_startup(bot: Bot) -> None:
    async with TelegramGroupAPI() as group_api:
        print(await group_api.create(
            "a43aa202-8827-4875-aa0f-963df7266da7",
            CreateTelegramGroup(
                telegramId=-100,
                source=TelegramSource.GROUP
            )
        ))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        settings.WEBHOOK_URL,
        drop_pending_updates=True,
        secret_token=settings.TELEGRAM_SECRET.get_secret_value()
    )


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    dispatcher.include_router(main_router)
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode=ParseMode.HTML)
