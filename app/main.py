from app.bot.factory import create_bot, create_dispatcher
from app.api.factory import create_app
from app.settings import settings

bot = create_bot(token=settings.TOKEN.get_secret_value())
dispatcher = create_dispatcher()
app = create_app(
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=settings.TELEGRAM_SECRET.get_secret_value(),
)
