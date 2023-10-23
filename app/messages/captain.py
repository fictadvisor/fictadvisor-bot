from app.messages.environment import environment

BROADCAST_CAPTAIN = environment.from_string("""
<b>Заявка на старосту</b>

<b>Від:</b> {{ data.last_name }} {{ data.first_name }} {{ data.middle_name|d('', true) }}

{% if user %}
<b>Юзернейм:</b> <a href="tg://user?id={{ user.id }}">{{ user.username|d(user.first_name, true) }}</a>
{% endif %}
<b>Група:</b> {{ data.group_code }}
""")
