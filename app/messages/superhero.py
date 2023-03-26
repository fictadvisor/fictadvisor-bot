from jinja2 import Environment

environment = Environment(trim_blocks=True, enable_async=True)

BROADCAST_SUPERHERO = environment.from_string("""
<b>Заявка на супергероя</b>

<b>Від:</b> {{ data.last_name }} {{ data.first_name }} {{ data.middle_name|d('', true) }}

{% if user %}
<b>Юзернейм:</b> <a href="tg://user?id=${user.id}">{{ user.username|d(user.first_name, true) }}</a>
{% endif %}
<b>Група:</b> {{ data.group_code }}
<b>Гуртожиток:</b> {{ "так" if data.dorm else "ні" }}
""")
