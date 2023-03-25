from jinja2 import Environment

environment = Environment(enable_async=True)

BROADCAST_RESPONSE = environment.from_string("""
<b>Відгук</b>

<b>QuestionId:</b> {{ data.question_id }}
<b>Предмет:</b> {{ data.subject }}
<b>Викладач:</b> {{ data.teacher_name }}
<b>UserId:</b> {{ data.user_id }}
<b>Від:</b> {{ user.lastName }} {{ user.firstName }} {{ user.middleName|d('', true) }}
<b>Відгук:</b> {{ data.response }}
""")
