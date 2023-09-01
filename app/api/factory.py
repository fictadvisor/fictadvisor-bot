from typing import Any

from aiogram import Bot, Dispatcher
from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middlewares.authentication import verify_token
from app.api.routes.broadcast import broadcast_router
from app.api.routes.captain import captain_router
from app.api.routes.response import response_router
from app.api.routes.student import student_router
from app.api.routes.superhero import superhero_router
from app.api.routes.webhook import webhook_router
from app.api.stubs import BotStub, DispatcherStub, SecretStub
from app.settings import settings


def create_app(bot: Bot, dispatcher: Dispatcher, webhook_secret: str) -> FastAPI:
    app = FastAPI()

    app.dependency_overrides.update(
        {
            BotStub: lambda: bot,
            DispatcherStub: lambda: dispatcher,
            SecretStub: lambda: webhook_secret,
        }
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(webhook_router)

    api = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_token)])
    for router in [response_router, student_router, superhero_router, captain_router, broadcast_router]:
        api.include_router(router)

    workflow_data = {
        "app": app,
        "dispatcher": dispatcher,
        "bot": bot,
        **dispatcher.workflow_data,
    }

    async def on_startup(*a: Any, **kw: Any) -> None:  # pragma: no cover
        await dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(*a: Any, **kw: Any) -> None:  # pragma: no cover
        await dispatcher.emit_shutdown(**workflow_data)

    if settings.USE_WEBHOOK:
        app.add_event_handler('startup', on_startup)
        app.add_event_handler('shutdown', on_shutdown)

    app.include_router(api)

    return app
