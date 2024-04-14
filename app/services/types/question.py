from app.services.types.base import Base
from pydantic import Field
from typing import Optional

class Question(Base):
    id: str
    order: int
    category: Optional[str] = None
    name: str
    description: Optional[str] = None
    text: str
    is_required: bool = Field(alias="isRequired")
    criteria: Optional[str] = None
    type: str #yet
    display: str #yet