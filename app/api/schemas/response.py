from uuid import UUID

from pydantic import Field, BaseModel


class BroadcastResponse(BaseModel):
    discipline_teacher_id: UUID = Field(..., alias="disciplineTeacherId")
    subject: str
    teacher_name: str = Field(..., alias="teacherName")
    user_id: UUID = Field(..., alias="userId")
    response: str
    question_id: UUID = Field(..., alias="questionId")
