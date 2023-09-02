from pydantic import BaseModel, Field


class UpdateTelegramGroup(BaseModel):
    telegram_id: int = Field(alias="telegramId")
