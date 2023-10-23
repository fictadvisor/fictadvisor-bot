from app.messages.environment import environment

BROADCAST_RESPONSE = environment.from_string("""
<b>Відгук</b>

<b>QuestionId:</b> <code>{{ data.question_id }}</code>
<b>DisciplineTeacherId:</b> <code>{{ data.discipline_teacher_id }}</code>
<b>Предмет:</b> {{ data.subject }}
<b>Викладач:</b> {{ data.teacher_name }}
<b>Відгук:</b> <code>{{ data.response }}</code>
""")
