from jinja2 import Environment

from app.utils.get_discipline_type_name import get_discipline_type_name

environment = Environment(enable_async=True, trim_blocks=True)
environment.globals.update(get_discipline_type_name=get_discipline_type_name)
