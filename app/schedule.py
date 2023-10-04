import asyncio
from asyncio import sleep
from datetime import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore

from app.messages.events import BROADCAST_EVENT
from app.services.group_api import GroupAPI
from app.services.schedule_api import ScheduleAPI
from app.services.types.group import GroupWithTelegramGroupsResponse


class Schedule:
    def __init__(self, bot: Bot):
        self._bot = bot
        self._scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self._scheduler.add_job(self.schedule, 'cron', second="02", minute="*", args=(self._bot,))
        self._scheduler.start()

    @staticmethod
    async def schedule_group(group: GroupWithTelegramGroupsResponse, bot: Bot) -> None:
        now = datetime.now()
        async with ScheduleAPI() as schedule_api:
            groups_to_send = filter(lambda x: x.post_info, group.telegram_groups)
            events = await schedule_api.get_general_group_events_by_day(group.id)

            for telegram_group in groups_to_send:
                for event in events.events:
                    delta = (event.start_time.hour - now.hour) * 60 + event.start_time.minute - now.minute
                    if delta == 5:
                        await bot.send_message(
                            telegram_group.telegram_id,
                            await BROADCAST_EVENT.render_async(delta="5 хвилин", event=event),
                            telegram_group.thread_id
                        )
                    elif delta == 15:
                        await bot.send_message(
                            telegram_group.telegram_id,
                            await BROADCAST_EVENT.render_async(delta="15 хвилин", event=event),
                            telegram_group.thread_id
                        )
                    await sleep(0.2)

    async def schedule(self, bot: Bot) -> None:
        async with GroupAPI() as group_api:
            groups = await group_api.get_groups_with_telegram_groups()
            await asyncio.gather(*(self.schedule_group(group, bot) for group in groups.groups if group.telegram_groups))
