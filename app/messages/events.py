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
<code>{{ start_hour + 2 }}:{{ "%02d" | format(start_minute) }}-{{ end_hour + 2 }}:{{ "%02d" | format(end_minute) }}</code>
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
{% for (start_time, end_time), now in group_by_time(day) %}
<code>{{ convert_to_time(start_time) }}-{{ convert_to_time(end_time) }}</code>
{% for event in now %}
<a href="{{ event.url|d('', true) }}">{{ get_discipline_type_name(event.discipline_type.name) }} {{ event.name }}</a>
{% endfor %}

{% endfor %}
{% endfor %}
""")

NOW_EVENT = environment.from_string("""
{% if group %}
Група: {{ group }}
{% endif %}
🔵 Лекція 🟠 Практика 🟢 Лаба

Станом на зараз:
<code>{{ convert_to_time(event_time[0]) }}-{{ convert_to_time(event_time[1]) }}</code>
{% for event in events %}
<a href="{{ event.url|d('', true) }}">{{ get_discipline_type_name(event.discipline_type.name) }} {{ event.name }}</a>
{% endfor %}
До кінця пари: <b>{% if time_left[0] %}{{ time_left[0] }} год {% endif %}{{ time_left[1] }} хв</b>
""")

LEFT_EVENT = environment.from_string("""
До кінця пари: <b>{% if time_left[0] %}{{ time_left[0] }} год {% endif %}{{ time_left[1] }} хв</b>
""")

NEXT_EVENT = environment.from_string("""
Наступнa пара:
<code>{{ convert_to_time(event_time[0]) }}-{{ convert_to_time(event_time[1]) }}</code>
{% for event in events %}
<a href="{{ event.url|d('', true) }}">{{ get_discipline_type_name(event.discipline_type.name) }} {{ event.name }}</a>
{% endfor %}
""")
