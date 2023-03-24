from typing import Annotated

from fastapi import status, Header, HTTPException

from app.settings import settings


async def verify_token(authorization: Annotated[str, Header()]):
    if authorization != f"Telegram {settings.TOKEN.get_secret_value()}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return authorization
