from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.settings import settings

auth_header = APIKeyHeader(
    name="Authorization",
    scheme_name="Bearer",
    description="Token of Telegram Bot",
    auto_error=False
)


async def verify_token(token: str = Security(auth_header)) -> str:
    if token != f"Bearer {settings.TOKEN.get_secret_value()}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return token
