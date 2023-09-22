from app.messages.environment import environment

BROADCAST_EVENT = environment.from_string("""
Через {{ delta }} хвилин розпочинається {{ get_discipline_type_name(event.discipline_type.name) }} з "{{ event.name }}"
{% if event.url %}
Посилання: {{ event.url }}
{% endif %}
""")
