from app.services.types.base import Base
from app.services.types.question import Question
from typing import List

class Category(Base):
    name: str
    count: int
    questions: List[Question]