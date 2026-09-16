"""Redis 멀티턴 채팅 API 모델입니다."""

from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    conversation_id: UUID | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    user_message: str
    assistant_message: str
    model: str
    context_messages: int
    ttl_seconds: int


class ConversationMessage(BaseModel):
    role: str
    content: str
