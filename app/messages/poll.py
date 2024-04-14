from app.messages.environment import environment

POLL_QUESTION = environment.from_string("""
{% if category %}
<b><i>{{category}}</i></b>
{% endif %}

<b>{{name}}</b>

{% if description %}
<b><i>{{description}}</i></b>
{% endif %}

{% if criteria %}
<i>{{criteria}}</i>
{% endif %}
""")
