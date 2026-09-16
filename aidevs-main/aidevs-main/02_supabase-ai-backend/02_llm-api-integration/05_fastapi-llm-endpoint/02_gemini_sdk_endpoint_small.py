r"""FastAPI + Gemini SDK 최소 endpoint 예제입니다.

이 파일은 예외 처리, key placeholder 검사, 자세한 오류 안내를 일부러 넣지 않습니다.
FastAPI endpoint 안에서 Gemini SDK를 호출하는 가장 작은 구조를 먼저 확인하기 위한 예제입니다.

주의:
    이 파일은 GEMINI_API_KEY가 설정되어 있으면 실제 Gemini API를 호출합니다.
    실제 호출은 무료 한도, quota, billing 상태에 따라 비용 또는 제한의 영향을 받을 수 있습니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\05_fastapi-llm-endpoint
    ..\..\.venv\Scripts\Activate.ps1
    uvicorn 02_gemini_sdk_endpoint_small:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 02_gemini_sdk_endpoint_small:app --reload

"""

from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field
from google import genai


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


app = FastAPI(title="Gemini SDK Small LLM Endpoint")


class ChatRequest(BaseModel):
    """프론트엔드나 API client가 보낼 채팅 요청 모델입니다."""

    message: str = Field(min_length=1, max_length=500, examples=["FastAPI에서 Pydantic을 왜 사용하나요?"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ai/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=request.message,
    )

    return {
        "provider": "gemini",
        "model": model,
        "actual_api_called": True,
        "answer": response.text,
    }
