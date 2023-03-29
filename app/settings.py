from typing import Optional

from pydantic import BaseSettings, SecretStr, AnyUrl, PositiveInt


class Settings(BaseSettings):
    LOG_LEVEL: Optional[str]
    LOG_FORMAT: Optional[str]

    TOKEN: SecretStr
    CHAT_ID: PositiveInt
    TELEGRAM_SECRET: SecretStr
    BASE_URL: AnyUrl
    FRONT_BASE_URL: AnyUrl
    WEBHOOK_PATH: str

    API_URL: AnyUrl

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.BASE_URL}{self.WEBHOOK_PATH}"

    class Config:
        env_file = ".env", "stack.env"
        env_file_encoding = "utf-8"


settings = Settings()
