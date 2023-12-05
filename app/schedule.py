import asyncio
import logging
from asyncio import sleep
from datetime import datetime

import pytz
from aiogram import Bot
from aiogram.exceptions import DetailedAiogramError
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED  # type: ignore
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore

from app.messages.events import BROADCAST_EVENTS, STARTING_EVENTS
from app.services.group_api import GroupAPI
from app.services.schedule_api import ScheduleAPI
from app.services.types.group import GroupWithTelegramGroupsResponse
from app.utils.events import group_by_time


class Schedule:
    def __init__(self, bot: Bot):
        self._bot = bot
        self._scheduler = AsyncIOScheduler()

    @staticmethod
    def error_handling(event) -> None:  # type: ignore
        if event.exception:
            logging.exception(event.exception)

    def start(self) -> None:
        self._scheduler.add_listener(self.error_handling, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._scheduler.add_job(self.schedule, 'cron', second="02", minute="*", args=(self._bot,))
        self._scheduler.start()

    @staticmethod
    async def schedule_group(group: GroupWithTelegramGroupsResponse, bot: Bot) -> None:
        now = datetime.now(tz=pytz.UTC)
        async with ScheduleAPI() as schedule_api:
            groups_to_send = list(filter(lambda x: x.post_info, group.telegram_groups))
            general_events = await schedule_api.get_general_group_events_by_day(group.id)
            grouped = group_by_time(general_events.events)

            for (start_time, _end_time), events in grouped:
                delta = (start_time - now).seconds // 60
                message = None
                if delta == 0:
                    message = await STARTING_EVENTS.render_async(events=events)
                elif delta == 14:
                    message = await BROADCAST_EVENTS.render_async(delta="15 хвилин", events=events)
                if message:
                    for telegram_group in groups_to_send:
                        try:
                            await bot.send_message(telegram_group.telegram_id, message, telegram_group.thread_id, disable_web_page_preview=True)
                        except DetailedAiogramError as e:
                            logging.error(e)
                        await sleep(0.2)

    async def schedule(self, bot: Bot) -> None:
        async with GroupAPI() as group_api:
            groups = await group_api.get_groups_with_telegram_groups()
            await asyncio.gather(*(self.schedule_group(group, bot) for group in groups.groups if group.telegram_groups))
