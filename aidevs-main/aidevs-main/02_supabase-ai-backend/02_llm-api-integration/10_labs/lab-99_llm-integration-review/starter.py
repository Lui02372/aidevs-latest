"""Lab 99 starter: mock-first LLM API 연동 흐름 종합 복습.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
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
    # TODO: 사용자 메시지와 AI 메시지를 messages_for_storage에 담아 반환하세요.
    # 이후 실제 프로젝트에서는 이 위치에서 Gemini SDK 호출 함수로 연결합니다.
    return ChatResponse(
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=False,
        answer="TODO",
        messages_for_storage=[],
    )


@app.post("/ai/chat-with-history", response_model=ChatResponse)
def chat_with_history(request: ChatWithHistoryRequest) -> ChatResponse:
    """이전 대화 이력을 참고한 mock 응답을 반환합니다."""
    # TODO: 기존 history 뒤에 새 사용자 메시지와 AI 메시지를 이어 붙이세요.
    # 이후 실제 프로젝트에서는 history를 Gemini contents 구조로 변환해 SDK에 전달합니다.
    return ChatResponse(
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=False,
        answer="TODO",
        messages_for_storage=[],
    )
