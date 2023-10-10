from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.bot.handlers import router as main_router
from app.bot.middlewares.throttling import ThrottlingMiddleware
from app.schedule import Schedule
from app.settings import settings
from app.utils.commands import set_bot_commands


async def on_startup(bot: Bot) -> None:
    schedule = Schedule(bot)
    schedule.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await set_bot_commands(bot)
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

    dispatcher.update.middleware(ThrottlingMiddleware())

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode=ParseMode.HTML)
