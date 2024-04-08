from typing import Dict, Optional, Union
from uuid import UUID

from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.certain_event import CertainEvent
from app.services.types.general_event import VerifyEvent
from app.services.types.general_events import FortnightGeneralEvents, GeneralEvents


class ScheduleAPI(BaseAPI):
    _path = "/schedule"

    async def get_general_group_events_by_day(self, group_id: Union[UUID, str], user_id: Optional[Union[UUID, str]] = None, day: Optional[int] = None, week: Optional[int] = None) -> GeneralEvents:
        params: Dict[str, Union[int, str]] = {}
        if day:
            params.update({"day": day})
        if user_id:
            params.update({"userId": str(user_id)})
        if week:
            params.update({"week": week})
        async with self._session.get(
            f"{self.path}/groups/{group_id}/day",
            params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return GeneralEvents.model_validate(json)
            raise ResponseException.from_json(json)

    async def get_general_group_events_by_week(self, group_id: Union[UUID, str], user_id: Optional[Union[UUID, str]] = None, week: Optional[int] = None) -> GeneralEvents:
        params: Dict[str, Union[int, str]] = {}
        if week:
            params.update({"week": week})
        if user_id:
            params.update({"userId": str(user_id)})
        async with self._session.get(
                f"{self.path}/groups/{group_id}/week",
                params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return GeneralEvents.model_validate(json)
            raise ResponseException.from_json(json)

    async def get_general_group_events_by_fortnight(self, group_id: Union[UUID, str], user_id: Optional[Union[UUID, str]] = None, week: Optional[int] = None) -> FortnightGeneralEvents:
        params: Dict[str, Union[int, str]] = {}
        if week:
            params.update({"week": week})
        if user_id:
            params.update({"userId": str(user_id)})
        async with self._session.get(
                f"{self.path}/groups/{group_id}/fortnight",
                params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return FortnightGeneralEvents.model_validate(json)
            raise ResponseException.from_json(json)

    async def get_certain_event(self, event_id: Union[UUID, str], group_id: Union[UUID, str], week: int) -> CertainEvent:
        params: Dict[str, Union[int, str]] = {}
        params.update({"week": week})
        async with self._session.get(
            f"{self.path}/groups/{group_id}/events/{event_id}",
            params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return CertainEvent.model_validate(json)
            raise ResponseException.from_json(json)

    async def add_event_info(self, event_id: Union[UUID, str], group_id: Union[UUID, str], verify_event: VerifyEvent) -> None:
        async with self._session.patch(
                f"{self.path}/groups/{group_id}/events/{event_id}",
                json=verify_event.model_dump(mode="json", by_alias=True)
        ) as response:
            json = await response.json(content_type=None)
            if response.status != 200:
                raise ResponseException.from_json(json)
