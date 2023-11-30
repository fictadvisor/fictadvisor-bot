from datetime import datetime

from jinja2 import Environment

from app.utils.date_service import DateService
from app.utils.events import get_weekday_name, group_by_time, group_by_weekday
from app.utils.get_discipline_type_name import get_discipline_type_name


async def convert_to_time(time: datetime) -> str:
    return DateService.add_tz_offset(time).strftime("%H:%M")

environment = Environment(enable_async=True, trim_blocks=True, autoescape=True)
environment.globals.update(
    get_discipline_type_name=get_discipline_type_name,
    group_by_time=group_by_time,
    group_by_weekday=group_by_weekday,
    get_weekday_name=get_weekday_name,
    convert_to_time=convert_to_time
)
