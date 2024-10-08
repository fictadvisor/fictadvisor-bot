from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation

from app.bot.handlers import router as main_router
from app.bot.middlewares.throttling import ThrottlingMiddleware
from app.bot.scenes.poll import PollScene
from app.schedule import Schedule
from app.settings import settings
from app.utils.commands import set_bot_commands


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    schedule = Schedule(bot)
    schedule.start()
    if (await bot.get_webhook_info()).url != settings.WEBHOOK_URL:
        await bot.delete_webhook(drop_pending_updates=True)
        await set_bot_commands(bot)
        await bot.set_webhook(
            settings.WEBHOOK_URL,
            drop_pending_updates=True,
            secret_token=settings.TELEGRAM_SECRET.get_secret_value(),
            allowed_updates=dispatcher.resolve_used_update_types()
        )


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation()
    )
    dispatcher.include_router(main_router)
    dispatcher.startup.register(on_startup)

    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(PollScene)

    dispatcher.update.middleware(ThrottlingMiddleware())

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ))
