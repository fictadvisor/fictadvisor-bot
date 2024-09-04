from pydantic import Field

from app.services.types.base import Base


class Answer(Base):
    question_id: str = Field(alias="questionId")
    value: str = Field(alias="value")

    def __hash__(self) -> int:
        hash_value = 0
        for char in self.question_id:
            hash_value = (hash_value * 31 + ord(char)) % (10**9 + 7)
        return hash_value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Answer):
            return NotImplemented
        return self.question_id == other.question_id
