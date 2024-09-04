from app.messages.environment import environment

POLL_QUESTION = environment.from_string("""
<b>{{question.name}}</b>

{% if question.description %}
<b><i>{{question.description}}</i></b>
{% endif %}

{% if question.criteria %}
<i>{{question.criteria}}</i>
{% endif %}
""")

SUBMIT_MSG = environment.from_string("""
<b>Перевір чи все правильно</b>

{% for idx, (question, answer) in enumerate(zip(questions, answers)) %}
<b>{{idx+1}}. {{question.name}}</b>
Ваша відповідь: <i>{{answer.value}}</i>
{% endfor %}
""")
