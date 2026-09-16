"""Lab 99 solution: mock-first LLM API 연동 흐름 종합 복습.

??:
    uvicorn solution:app --reload

? ???? ??? ??:
    python -m uvicorn solution:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Lab 99 LLM Integration Review")


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
    """mock LLM 응답입니다."""

    provider: str
    model: str
    actual_api_called: bool
    answer: str
    messages_for_storage: list[Message]


@app.get("/health")
def health_check() -> dict:
    """서버 실행 상태를 확인합니다."""
    return {"status": "ok"}


@app.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """단일 질문에 대한 mock 응답을 반환합니다."""
    if request.memo_context:
        answer = f"메모를 참고해 답변합니다: {request.memo_context} / 질문: {request.message}"
    else:
        answer = f"질문을 확인했습니다: {request.message}"

    messages_for_storage = [
        Message(role="user", content=request.message),
        Message(role="assistant", content=answer),
    ]

    return ChatResponse(
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=False,
        answer=answer,
        messages_for_storage=messages_for_storage,
    )


@app.post("/ai/chat-with-history", response_model=ChatResponse)
def chat_with_history(request: ChatWithHistoryRequest) -> ChatResponse:
    """이전 대화 이력을 참고한 mock 응답을 반환합니다."""
    previous_count = len(request.history)
    answer = (
        f"이전 대화 {previous_count}개를 참고했습니다. "
        f"새 질문 '{request.message}'에 대해 이어서 답변합니다."
    )

    messages_for_storage = [
        *request.history,
        Message(role="user", content=request.message),
        Message(role="assistant", content=answer),
    ]

    return ChatResponse(
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=False,
        answer=answer,
        messages_for_storage=messages_for_storage,
    )
