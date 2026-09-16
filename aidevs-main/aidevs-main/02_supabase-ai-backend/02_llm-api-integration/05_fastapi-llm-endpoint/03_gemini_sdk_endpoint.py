r"""FastAPI + Gemini SDK endpoint 예제입니다.

이 파일은 05_fastapi-llm-endpoint 단원의 실제 프로젝트 기본 구현입니다.
02_gemini_sdk_endpoint_small.py보다 요청 모델, 응답 모델, key 확인, 오류 안내를 더 포함합니다.

흐름:
    사용자 요청
    -> FastAPI endpoint
    -> Pydantic 요청 검증
    -> Gemini SDK 호출
    -> JSON 응답 반환

이후 단원에서는 이 응답을 Supabase 대화 이력과 서비스 로그로 저장하는 방향으로 확장합니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\05_fastapi-llm-endpoint
    ..\..\.venv\Scripts\Activate.ps1
    uvicorn 03_gemini_sdk_endpoint:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 03_gemini_sdk_endpoint:app --reload

"""

from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


app = FastAPI(
    title="Gemini SDK LLM Endpoint",
    description="FastAPI endpoint에서 Gemini SDK를 호출하는 기본 프로젝트 구조입니다.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    """프론트엔드나 API client가 보낼 채팅 요청 모델입니다."""

    message: str = Field(min_length=1, max_length=500, examples=["FastAPI에서 Pydantic을 왜 사용하나요?"])
    memo_context: str = Field(default="", max_length=1000, examples=["Pydantic은 요청 데이터를 검증합니다."])
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    max_output_tokens: int = Field(default=300, ge=50, le=1000)


class ChatResponse(BaseModel):
    """Gemini 응답을 클라이언트에 돌려줄 때 사용할 응답 모델입니다."""

    provider: str
    model: str
    actual_api_called: bool
    answer: str


def is_real_api_key(value: str | None) -> bool:
    """API key가 비어 있지 않고 예시 값도 아닌지 확인합니다."""

    key = (value or "").strip()

    if not key:
        return False

    return not key.startswith(("your-", "your_", "sk-your", "AIza-your"))


def format_gemini_error(error: Exception, model: str) -> str:
    """Gemini API 호출 오류를 API 응답 메시지로 정리합니다."""

    status_code = getattr(error, "status_code", None)
    message = str(error)

    if status_code == 503 or "UNAVAILABLE" in message or "high demand" in message:
        return (
            f"Gemini API 호출에 실패했습니다. 사용 모델: {model}. "
            "Gemini 서버가 일시적으로 바쁘거나 해당 모델 수요가 높은 상태입니다. "
            "잠시 뒤 다시 실행하거나 .env의 GEMINI_MODEL을 다른 사용 가능한 모델로 바꿔 보세요."
        )

    if status_code == 429 or "RESOURCE_EXHAUSTED" in message:
        return (
            f"Gemini API 호출에 실패했습니다. 사용 모델: {model}. "
            "호출 횟수 또는 quota/rate limit에 도달했을 수 있습니다. "
            "Google AI Studio에서 현재 quota와 rate limit을 확인하세요."
        )

    if status_code in {400, 401, 403}:
        return (
            f"Gemini API 호출에 실패했습니다. 사용 모델: {model}. "
            "API key, 모델 이름, 권한 설정 중 하나가 잘못되었을 수 있습니다. "
            ".env의 GEMINI_API_KEY와 GEMINI_MODEL 값을 다시 확인하세요."
        )

    return f"Gemini API 호출 중 예기치 않은 오류가 발생했습니다. 원본 오류: {message}"


def build_prompt(request: ChatRequest) -> str:
    """사용자 질문과 참고 메모를 Gemini에 보낼 하나의 프롬프트로 정리합니다."""

    parts = ["당신은 Python과 FastAPI를 쉽게 설명하는 학습 도우미입니다."]
    if request.memo_context:
        parts.append(f"참고 메모:\n{request.memo_context}")
    parts.append(f"사용자 질문:\n{request.message}")
    parts.append("답변은 초보자가 이해할 수 있도록 단계별로 작성해 주세요.")
    return "\n\n".join(parts)


@app.get("/health")
def health_check() -> dict[str, str]:
    """서버 상태 확인용 API입니다."""

    return {"status": "ok"}


@app.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """FastAPI 요청을 받아 Gemini SDK 호출 흐름으로 연결합니다."""

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    if not is_real_api_key(api_key):
        return ChatResponse(
            provider="gemini",
            model=model,
            actual_api_called=False,
            answer="GEMINI_API_KEY가 없거나 placeholder 값입니다. 01_mock_llm_endpoint.py로 먼저 구조를 확인하세요.",
        )

    try:
        from google import genai
    except ModuleNotFoundError:
        return ChatResponse(
            provider="gemini",
            model=model,
            actual_api_called=False,
            answer="google-genai 패키지가 설치되어 있지 않습니다. pip install -r requirements.txt를 먼저 실행하세요.",
        )

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=model,
            contents=build_prompt(request),
            config={
                "temperature": request.temperature,
                "max_output_tokens": request.max_output_tokens,
            },
        )
    except Exception as error:
        return ChatResponse(
            provider="gemini",
            model=model,
            actual_api_called=True,
            answer=format_gemini_error(error, model),
        )

    return ChatResponse(
        provider="gemini",
        model=model,
        actual_api_called=True,
        answer=response.text,
    )
