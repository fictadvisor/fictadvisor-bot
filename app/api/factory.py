from functools import partial

from aiogram import Dispatcher, Bot
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.middlewares.authentication import verify_token
from app.api.routes.response import response_router
from app.api.routes.student import student_router
from app.api.routes.superhero import superhero_router
from app.api.routes.webhook import webhook_router
from app.api.stubs import BotStub, DispatcherStub, SecretStub
from app.custom_logging import CustomizeLogger
from app.settings import settings


async def on_startup(bot: Bot):
    webhook_info = await bot.get_webhook_info()
    if webhook_info != settings.WEBHOOK_URL:
        await bot.set_webhook(
            settings.WEBHOOK_URL,
            drop_pending_updates=True,
            secret_token=settings.TELEGRAM_SECRET.get_secret_value()
        )


async def on_shutdown(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)


def create_app(bot: Bot, dispatcher: Dispatcher, webhook_secret: str) -> FastAPI:
    app = FastAPI()

    app.dependency_overrides.update(
        {
            BotStub: lambda: bot,
            DispatcherStub: lambda: dispatcher,
            SecretStub: lambda: webhook_secret,
        }
    )
    logger = CustomizeLogger.make_logger(settings.LOG_LEVEL, settings.LOG_FORMAT)
    app.logger = logger

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler('startup', partial(on_startup, bot))
    app.add_event_handler('shutdown', partial(on_shutdown, bot))
    app.include_router(webhook_router)

    api = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_token)])
    for router in [response_router, student_router, superhero_router]:
        api.include_router(router)

    app.include_router(api)

    return app
