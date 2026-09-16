"""Notes API에서 사용하는 Pydantic 모델입니다."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """POST /notes 요청 Body입니다."""

    # Field의 min_length는 빈 문자열을 막습니다.
    # examples는 Swagger UI에서 예시 입력값으로 표시됩니다.
    title: str = Field(min_length=1, examples=["FastAPI 구조 정리"])
    content: str = Field(min_length=1, examples=["router, schema, service를 나누어 봅니다."])


class NoteUpdate(BaseModel):
    """PUT /notes/{note_id} 요청 Body입니다."""

    title: str = Field(min_length=1, examples=["수정된 제목"])
    content: str = Field(min_length=1, examples=["수정된 내용"])


class NotePublic(BaseModel):
    """클라이언트에 반환하는 노트 응답 모델입니다."""

    # DB 내부 row를 그대로 반환하지 않고, 화면/API에 공개할 필드만 모델로 정의합니다.
    id: UUID
    title: str
    content: str
    created_at: datetime | None = None
