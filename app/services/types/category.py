from typing import List

from app.services.types.base import Base
from app.services.types.question import Question


class Category(Base):
    name: str
    count: int
    questions: List[Question]
