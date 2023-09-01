from typing import Optional

from pydantic import AnyUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: Optional[str]
    LOG_FORMAT: Optional[str]

    USE_WEBHOOK: bool = True

    TOKEN: SecretStr
    CHAT_ID: int
    TELEGRAM_SECRET: SecretStr
    BASE_URL: AnyUrl
    FRONT_BASE_URL: AnyUrl
    WEBHOOK_PATH: str

    API_URL: AnyUrl

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.BASE_URL}{self.WEBHOOK_PATH}"

    model_config = SettingsConfigDict(env_file=('.env', 'stack.env'), env_file_encoding='utf-8', extra='ignore')


settings = Settings()
