from aiogram import F, Router

from app.bot.handlers.verification.captain import approve_captain, deny_captain
from app.bot.handlers.verification.response import approve_response, deny_response
from app.bot.handlers.verification.student import approve_student, deny_student
from app.bot.handlers.verification.superhero import approve_superhero, deny_superhero
from app.bot.schemas.captain import CaptainData
from app.bot.schemas.response import ResponseData
from app.bot.schemas.student import StudentData
from app.bot.schemas.superhero import SuperheroData
from app.services.user_api import State

router = Router(name=__name__)

router.callback_query.register(approve_captain, CaptainData.filter(F.method == State.APPROVED))
router.callback_query.register(deny_captain, CaptainData.filter(F.method == State.DECLINED))

router.callback_query.register(approve_response, ResponseData.filter(F.method == State.APPROVED))
router.callback_query.register(deny_response, ResponseData.filter(F.method == State.DECLINED))

router.callback_query.register(approve_student, StudentData.filter(F.method == State.APPROVED))
router.callback_query.register(deny_student, StudentData.filter(F.method == State.DECLINED))

router.callback_query.register(approve_superhero, SuperheroData.filter(F.method == State.APPROVED))
router.callback_query.register(deny_superhero, SuperheroData.filter(F.method == State.DECLINED))