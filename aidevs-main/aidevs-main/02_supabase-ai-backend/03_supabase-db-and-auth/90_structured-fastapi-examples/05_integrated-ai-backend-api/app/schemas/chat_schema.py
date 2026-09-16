"""채팅 요청/응답 모델입니다."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """POST /chat 요청 Body입니다."""

    message: str = Field(min_length=1, examples=["Redis 캐시는 언제 쓰나요?"])


class ChatResponse(BaseModel):
    """POST /chat 응답 모델입니다."""

    user_message: str
    assistant_message: str
    # cached=True이면 Redis에 저장된 기존 답변을 재사용했다는 뜻입니다.
    cached: bool
    provider: str
    model: str
    actual_api_called: bool
    log_id: str | None = None


class ChatLogPublic(BaseModel):
    """GET /logs에서 반환하는 로그 1건의 모델입니다."""

    id: str
    user_id: str
    user_message: str
    assistant_message: str | None = None
    provider: str
    model: str | None = None
    actual_api_called: bool
    cached: bool
    status: str
    error_message: str | None = None
    created_at: str | None = None
