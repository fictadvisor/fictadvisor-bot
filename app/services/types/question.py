from typing import Optional

from pydantic import Field

from app.enums.poll import DisplayType, QuestionType
from app.services.types.base import Base


class Question(Base):
    id: str
    order: int
    category: Optional[str] = None
    name: str
    description: Optional[str] = None
    text: str
    is_required: bool = Field(alias="isRequired")
    criteria: Optional[str] = None
    type: QuestionType
    display: DisplayType
