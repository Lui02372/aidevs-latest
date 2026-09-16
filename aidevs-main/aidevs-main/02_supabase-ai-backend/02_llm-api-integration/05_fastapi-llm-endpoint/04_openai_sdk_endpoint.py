r"""FastAPI + OpenAI SDK endpoint 예제입니다.

OPENAI_API_KEY가 없으면 실제 API를 호출하지 않고 안내 메시지를 반환합니다.
OPENAI_API_KEY가 있으면 실제 호출을 수행하므로 비용이 발생할 수 있습니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\05_fastapi-llm-endpoint
    ..\..\.venv\Scripts\Activate.ps1
    uvicorn 04_openai_sdk_endpoint:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 04_openai_sdk_endpoint:app --reload

"""

from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field


# 실제 API 호출이 필요하면 .env에 OPENAI_API_KEY를 넣은 뒤 이 예제를 실행합니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


app = FastAPI(title="OpenAI SDK LLM Endpoint")


class ChatRequest(BaseModel):
    """실제 API 호출에 사용할 요청 모델입니다."""

    message: str = Field(min_length=1, max_length=500, examples=["FastAPI에서 Pydantic을 왜 사용하나요?"])
    memo_context: str = Field(default="", max_length=1000, examples=["Pydantic은 요청 데이터를 검증합니다."])
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    max_tokens: int = Field(default=300, ge=50, le=1000)


def is_real_api_key(value: str | None) -> bool:
    """API key가 비어 있지 않고 예시 값도 아닌지 확인합니다."""

    key = (value or "").strip()

    if not key:
        return False

    return not key.startswith(("your-", "your_", "sk-your", "AIza-your"))


def build_user_content(request: ChatRequest) -> str:
    """OpenAI messages에 넣을 user content를 만듭니다."""

    parts = []
    if request.memo_context:
        parts.append(f"참고 메모:\n{request.memo_context}")
    parts.append(f"사용자 질문:\n{request.message}")
    return "\n\n".join(parts)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ai/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not is_real_api_key(api_key):
        return {
            "provider": "openai",
            "model": model,
            "actual_api_called": False,
            "answer": "OPENAI_API_KEY가 없거나 placeholder 값입니다. mock 예제로 먼저 실습하세요.",
        }

    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "당신은 Python과 FastAPI를 쉽게 설명하는 학습 도우미입니다."},
            {"role": "user", "content": build_user_content(request)},
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return {
        "provider": "openai",
        "model": model,
        "actual_api_called": True,
        "answer": response.choices[0].message.content,
    }
