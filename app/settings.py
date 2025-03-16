from typing import Optional

from pydantic import AnyUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEVELOPMENT: bool = False
    DEBUG: bool = True
    NGROK_AUTHTOKEN: Optional[SecretStr] = None

    TOKEN: SecretStr
    CHAT_ID: int
    ERRORS_CHAT_ID: int
    ERRORS_THREAD_ID: Optional[int] = None
    TELEGRAM_SECRET: SecretStr
    BASE_URL: AnyUrl = AnyUrl("http://localhost:8000")
    FRONT_BASE_URL: AnyUrl
    WEBHOOK_PATH: str = '/webhook'

    API_URL: AnyUrl
    API_ACCESS_TOKEN: SecretStr

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.BASE_URL}{self.WEBHOOK_PATH}"

    model_config = SettingsConfigDict(env_file=('.env', 'stack.env'), env_file_encoding='utf-8', extra='ignore')


settings = Settings()
