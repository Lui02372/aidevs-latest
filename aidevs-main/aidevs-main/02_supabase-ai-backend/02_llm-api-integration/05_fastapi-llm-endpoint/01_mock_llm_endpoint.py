r"""FastAPI + mock LLM endpoint 통합 예제입니다.

이 파일은 실제 Gemini 또는 OpenAI API를 호출하지 않습니다.
FastAPI가 사용자 질문을 받고, 메모 컨텍스트를 함께 정리한 뒤,
LLM 응답처럼 보이는 JSON을 반환하는 구조를 비용 없이 확인합니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\05_fastapi-llm-endpoint
    ..\..\.venv\Scripts\Activate.ps1
    uvicorn 01_mock_llm_endpoint:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 01_mock_llm_endpoint:app --reload

"""

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="FastAPI Mock LLM Endpoint",
    description="FastAPI endpoint에서 LLM 호출 흐름을 mock 응답으로 연습합니다.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    """프론트엔드나 API client가 보낼 채팅 요청 모델입니다."""

    message: str = Field(
        min_length=1,
        max_length=500,
        examples=["FastAPI에서 Pydantic을 왜 사용하나요?"],
    )
    memo_context: str = Field(
        default="",
        max_length=1000,
        examples=["Pydantic은 요청 데이터를 검증하고 응답 모델을 정리합니다."],
    )
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    max_tokens: int = Field(default=300, ge=50, le=1000)


class ChatResponse(BaseModel):
    """AI 응답을 클라이언트에 돌려줄 때 사용할 응답 모델입니다."""

    provider: str
    model: str
    actual_api_called: bool
    answer: str
    usage: dict[str, Any]


def build_prompt(request: ChatRequest) -> str:
    """사용자 질문과 메모 컨텍스트를 LLM에 전달할 프롬프트로 정리합니다."""

    prompt_parts = [
        "당신은 Python과 FastAPI를 쉽게 설명하는 학습 도우미입니다.",
    ]

    if request.memo_context:
        prompt_parts.append(f"참고 메모:\n{request.memo_context}")

    prompt_parts.append(f"사용자 질문:\n{request.message}")
    prompt_parts.append("답변은 초보자가 이해할 수 있도록 단계별로 작성해 주세요.")

    return "\n\n".join(prompt_parts)


def generate_mock_answer(prompt: str, temperature: float) -> str:
    """실제 모델 응답 대신 학습용 가짜 응답을 생성합니다."""

    return (
        "이 응답은 실제 LLM API가 아니라 mock 함수가 만든 답변입니다. "
        "FastAPI endpoint는 요청 Body를 검증하고, 필요한 컨텍스트를 붙인 뒤, "
        f"temperature={temperature} 설정과 함께 모델 호출 함수로 넘기는 구조로 확장됩니다.\n\n"
        f"입력 프롬프트 미리보기:\n{prompt[:180]}"
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    """서버 상태 확인용 API입니다."""

    return {"status": "ok"}


@app.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """AI 챗봇 endpoint의 기본 구조입니다."""

    prompt = build_prompt(request)
    answer = generate_mock_answer(prompt, request.temperature)

    return ChatResponse(
        provider="mock",
        model="mock-fastapi-llm",
        actual_api_called=False,
        answer=answer,
        usage={
            "input_length": len(prompt),
            "max_tokens": request.max_tokens,
        },
    )
