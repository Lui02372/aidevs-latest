"""Assignment 99 starter: FastAPI mock-first LLM 미니 서비스.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Assignment 99 Mock LLM Mini Service")


class Message(BaseModel):
    """대화 이력에 저장할 메시지 한 개입니다."""

    role: str = Field(..., description="user 또는 assistant")
    content: str = Field(..., min_length=1, description="메시지 내용")


class ChatRequest(BaseModel):
    """단일 질문 요청입니다."""

    message: str = Field(..., min_length=1)
    memo_context: str = ""


class ChatWithHistoryRequest(BaseModel):
    """이전 대화 이력을 포함한 요청입니다."""

    message: str = Field(..., min_length=1)
    history: list[Message] = []


class ChatResponse(BaseModel):
    """프론트엔드와 Supabase 저장 흐름을 고려한 응답 구조입니다."""

    provider: str
    model: str
    actual_api_called: bool
    answer: str
    messages_for_storage: list[Message]


@app.get("/health")
def health_check() -> dict:
    """서버가 실행 중인지 확인합니다."""
    return {"status": "ok"}


@app.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """single-turn mock 응답을 반환합니다."""
    # TODO: request.message와 request.memo_context를 활용해 answer를 만드세요.
    # TODO: user 메시지와 assistant 메시지를 messages_for_storage에 담으세요.
    # README에는 이 위치가 Gemini SDK 호출 함수로 교체될 수 있음을 설명하세요.
    return ChatResponse(
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=False,
        answer="TODO",
        messages_for_storage=[],
    )


@app.post("/ai/chat-with-history", response_model=ChatResponse)
def chat_with_history(request: ChatWithHistoryRequest) -> ChatResponse:
    """multi-turn mock 응답을 반환합니다."""
    # TODO: request.history 뒤에 새 user/assistant 메시지를 이어 붙이세요.
    # README에는 history를 Gemini contents 구조로 변환하는 기준을 설명하세요.
    return ChatResponse(
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=False,
        answer="TODO",
        messages_for_storage=[],
    )
