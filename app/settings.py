from pydantic import AnyUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEVELOPMENT: bool = False

    TOKEN: SecretStr
    CHAT_ID: int
    TELEGRAM_SECRET: SecretStr
    BASE_URL: AnyUrl = AnyUrl("http://localhost:8000")
    FRONT_BASE_URL: AnyUrl
    WEBHOOK_PATH: str

    API_URL: AnyUrl

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.BASE_URL}{self.WEBHOOK_PATH}"

    model_config = SettingsConfigDict(env_file=('.env', 'stack.env'), env_file_encoding='utf-8', extra='ignore')


settings = Settings()
