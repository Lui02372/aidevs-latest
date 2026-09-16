"""Lab 05 solution: FastAPI mock-first LLM 엔드포인트.

??:
    uvicorn solution:app --reload

? ???? ??? ??:
    python -m uvicorn solution:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Lab 05 Mock LLM API")


class ChatRequest(BaseModel):
    """사용자가 AI에게 보낼 요청 데이터입니다."""

    message: str = Field(..., min_length=1, description="사용자 질문")
    memo_context: str = Field(default="", description="AI가 참고할 메모 내용")
    temperature: float = Field(default=0.3, ge=0, le=2)
    max_tokens: int = Field(default=300, ge=1, le=1000)


class ChatResponse(BaseModel):
    """AI 응답을 프론트엔드가 이해하기 쉽게 정리한 구조입니다."""

    provider: str
    model: str
    actual_api_called: bool
    answer: str


@app.get("/health")
def health_check() -> dict:
    """서버가 실행 중인지 확인합니다."""
    return {"status": "ok"}


@app.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """사용자의 질문을 받아 mock AI 응답을 반환합니다."""
    # 실제 프로젝트에서는 이 위치에서 Gemini SDK 호출 함수로 연결합니다.
    if request.memo_context:
        answer = (
            f"메모 '{request.memo_context}'를 참고했습니다. "
            f"질문 '{request.message}'에 대해 핵심부터 정리해 보겠습니다."
        )
    else:
        answer = f"질문 '{request.message}'에 대해 핵심부터 정리해 보겠습니다."

    return ChatResponse(
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=False,
        answer=answer,
    )
