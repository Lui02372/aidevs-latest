"""LLM Chat API에서 사용하는 요청/응답 모델입니다."""

from pydantic import BaseModel, Field


class Message(BaseModel):
    """대화 이력에 저장할 메시지 한 개입니다."""

    role: str = Field(description="user 또는 assistant")
    content: str = Field(min_length=1, description="메시지 내용")


class ChatRequest(BaseModel):
    """POST /ai/chat 요청 Body 모델입니다."""

    message: str = Field(min_length=1, examples=["FastAPI에서 Pydantic을 왜 사용하나요?"])
    memo_context: str = Field(default="", examples=["Pydantic은 요청 데이터를 검증합니다."])


class ChatWithHistoryRequest(BaseModel):
    """POST /ai/chat-with-history 요청 Body 모델입니다."""

    message: str = Field(min_length=1, examples=["그 내용을 한 문장으로 요약해줘."])
    history: list[Message] = Field(default_factory=list)


class ChatResponse(BaseModel):
    """클라이언트와 Supabase 저장 흐름을 고려한 응답 모델입니다."""

    provider: str
    model: str
    actual_api_called: bool
    answer: str
    messages_for_storage: list[Message]
