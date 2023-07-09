from jinja2 import Environment

environment = Environment(enable_async=True)

BROADCAST_RESPONSE = environment.from_string("""
<b>Відгук</b>

<b>QuestionId:</b> <code>{{ data.question_id }}</code>
<b>Предмет:</b> {{ data.subject }}
<b>Викладач:</b> {{ data.teacher_name }}
<b>UserId:</b> <code>{{ data.user_id }}</code>
<b>Від:</b> {{ user.lastName }} {{ user.firstName }} {{ user.middleName|d('', true) }}
<b>Відгук:</b> <code>{{ data.response }}</code>
""")
