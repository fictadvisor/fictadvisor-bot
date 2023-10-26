from app.messages.environment import environment

STARTING_EVENTS = environment.from_string("""
{% if group %}
Група: {{ group }}
{% endif %}
🔵 Лекція 🟠 Практика 🟢 Лаба

Розпочалися пари:
{% for event in events %}
<a href="{{ event.url|d('', true) }}">{{ get_discipline_type_name(event.discipline_type.name) }} {{ event.name }}</a>
{% endfor %}
""")

BROADCAST_EVENTS = environment.from_string("""
{% if group %}
Група: {{ group }}
{% endif %}
🔵 Лекція 🟠 Практика 🟢 Лаба

Через {{ delta }} розпочинається:
{% for event in events %}
<a href="{{ event.url|d('', true) }}">{{ get_discipline_type_name(event.discipline_type.name) }} {{ event.name }}</a>
{% endfor %}
""")

EVENT_LIST = environment.from_string("""
{% if group %}
Група: {{ group }}
{% endif %}
🔵 Лекція 🟠 Практика 🟢 Лаба

{% for (start_hour, start_minute, end_hour, end_minute), now in group_by_time(events) %}
<i>{{ start_hour + 3 }}:{{ "%02d" | format(start_minute) }}-{{ end_hour + 3 }}:{{ "%02d" | format(end_minute) }}</i>
{% for event in now %}
<a href="{{ event.url|d('', true) }}">{{ get_discipline_type_name(event.discipline_type.name) }} {{ event.name }}</a>
{% endfor %}

{% endfor %}
""")

WEEK_EVENT_LIST = environment.from_string("""
{% if group %}
Група: {{ group }}
{% endif %}
🔵 Лекція 🟠 Практика 🟢 Лаба

{% for weekday, day in group_by_weekday(events) %}
<b>{{ get_weekday_name(weekday, week) }}</b>
{% for (start_hour, start_minute, end_hour, end_minute), now in group_by_time(day) %}
<i>{{ start_hour + 3 }}:{{ "%02d" | format(start_minute) }}-{{ end_hour + 3 }}:{{ "%02d" | format(end_minute) }}</i>
{% for event in now %}
<a href="{{ event.url|d('', true) }}">{{ get_discipline_type_name(event.discipline_type.name) }} {{ event.name }}</a>
{% endfor %}

{% endfor %}
{% endfor %}
""")
