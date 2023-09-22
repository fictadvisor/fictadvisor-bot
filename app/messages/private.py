from app.messages.environment import environment

START = environment.from_string("""
<b>Вітаємо вас у боті <a href="{{ front_url }}">fictadvisor.com</a></b>
Зворотній зв'язок: @fict_robot
""")

REGISTER = environment.from_string("""
<b>Для реєстрації перейдіть за посиланням</b>

Якщо кнопка не працює, тицьни <a href="{{ register_url }}">сюди</a>
""")
