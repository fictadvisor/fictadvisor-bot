from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import SecretStr
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, token: SecretStr):
        super().__init__(app)
        self.__token = token

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.headers.get("Authorization") != f"Telegram {self.__token.get_secret_value()}":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "message": "Unauthorized"
                }
            )

        return await call_next(request)
