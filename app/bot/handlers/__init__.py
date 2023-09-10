from aiogram import Router

from app.bot.handlers.debug import router as debug_router
from app.bot.handlers.group import router as group_router
from app.bot.handlers.private import router as private_router
from app.bot.handlers.schedule import router as schedule_router
from app.bot.handlers.verification import router as verification_router

router = Router(name=__name__)

router.include_routers(
    verification_router,
    private_router,
    debug_router,
    schedule_router,
    group_router
)
