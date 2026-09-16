"""멀티턴 대화 API의 요청과 응답 모델입니다."""

from pydantic import BaseModel, Field
from uuid import UUID


class ChatRequest(BaseModel):
    """새 질문과 선택적인 대화 ID입니다."""

    message: str = Field(min_length=1, max_length=1000, examples=["방금 설명을 예시로 다시 알려줘"])
    conversation_id: UUID | None = Field(
        default=None,
        description="이전 대화를 이어 갈 UUID입니다. 비우면 새 대화를 시작합니다.",
    )


class ChatResponse(BaseModel):
    """Gemini 답변과 현재 대화 ID를 반환합니다."""

    conversation_id: str
    user_message: str
    assistant_message: str
    model: str
    context_turns: int


class ChatMessage(BaseModel):
    """저장된 대화 1턴입니다."""

    id: str
    conversation_id: str
    user_message: str
    assistant_message: str
    model: str
    created_at: str | None = None
