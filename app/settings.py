from pydantic import BaseSettings, SecretStr, AnyUrl


class Settings(BaseSettings):
    TOKEN: SecretStr
    TELEGRAM_SECRET: SecretStr
    BASE_URL: AnyUrl
    WEBHOOK_PATH: str

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.BASE_URL}{self.WEBHOOK_PATH}"

    class Config:
        env_file = ".env", "stack.env"
        env_file_encoding = "utf-8"


settings = Settings()
