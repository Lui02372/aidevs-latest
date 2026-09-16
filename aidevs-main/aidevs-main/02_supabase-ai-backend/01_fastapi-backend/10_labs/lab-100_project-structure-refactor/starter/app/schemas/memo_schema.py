from pydantic import BaseModel, Field


class MemoCreate(BaseModel):
    """메모 생성 요청 모델입니다."""

    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


class MemoPublic(BaseModel):
    """API 응답으로 공개할 메모 모델입니다."""

    id: int
    title: str
    content: str
    tags: list[str]


class MemoListResponse(BaseModel):
    """메모 목록 응답 모델입니다."""

    count: int
    data: list[MemoPublic]
