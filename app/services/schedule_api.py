from typing import Optional
from uuid import UUID

from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.fortnight_general_events import FortnightGeneralEvents
from app.services.types.general_events import GeneralEvents


class ScheduleAPI(BaseAPI):
    _path = "schedule"

    async def get_general_group_events_by_day(self, group_id: UUID, day: Optional[int] = None) -> GeneralEvents:
        params = None
        if day:
            params = {"day": day}
        async with self._session.get(
            f"{self.path}/groups/{group_id}/general/day",
            params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return GeneralEvents.model_validate(json)
            raise ResponseException.from_json(json)

    async def get_general_group_events_by_week(self, group_id: UUID, week: Optional[int] = None) -> GeneralEvents:
        params = None
        if week:
            params = {"week": week}
        async with self._session.get(
                f"{self.path}/groups/{group_id}/general/week",
                params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return GeneralEvents.model_validate(json)
            raise ResponseException.from_json(json)

    async def get_general_group_events_by_fortnight(self, group_id: UUID, week: Optional[int] = None) -> FortnightGeneralEvents:
        params = None
        if week:
            params = {"week": week}
        async with self._session.get(
                f"{self.path}/groups/{group_id}/general/fortnight",
                params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return FortnightGeneralEvents.model_validate(json)
            raise ResponseException.from_json(json)
