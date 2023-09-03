from datetime import datetime
from typing import Any, Dict, Self

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class ResponseExceptionData(BaseModel):
    status: int
    timestamp: datetime
    error: str
    message: str


@dataclass
class ResponseException(Exception):
    status: int
    timestamp: datetime
    error: str
    message: str

    def __str__(self) -> str:
        return self.message

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> Self:
        return cls(
            **ResponseExceptionData
            .model_validate(json)
            .model_dump()
        )


