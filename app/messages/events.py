from app.messages.environment import environment

BROADCAST_EVENT = environment.from_string("""
Через {{ delta }} хвилин розпочинається {{ get_discipline_type_name(event.discipline_type.name) }} з "{{ event.name }}"
{% if event.url %}
Посилання: {{ event.url }}
{% endif %}
""")

EVENT_LIST = environment.from_string("""
{% for (start_hour, start_minute, end_hour, end_minute), now in group_by_time(events) %}
{{ start_hour }}:{{ "%02d" | format(start_minute) }}-{{ end_hour }}:{{ "%02d" | format(end_minute) }}
{% for event in now %}
{{ get_discipline_type_name(event.discipline_type.name)|title }}. {{ event.name }}
{% endfor %}

{% endfor %}
""")

WEEK_EVENT_LIST = environment.from_string("""
{% for weekday, day in group_by_weekday(events) %}
{{ get_weekday_name(weekday) }}
{% for (start_hour, start_minute, end_hour, end_minute), now in group_by_time(day) %}
{{ start_hour }}:{{ "%02d" | format(start_minute) }}-{{ end_hour }}:{{ "%02d" | format(end_minute) }}
{% for event in now %}
{{ get_discipline_type_name(event.discipline_type.name)|title }}. {{ event.name }}
{% endfor %}

{% endfor %}

{% endfor %}
""")
