"""FastAPI에서 Gemini와 대화하고 Supabase에 채팅 로그를 저장하는 예제입니다.

이 파일의 목적:
    Swagger에서 사용자가 질문을 입력하면 FastAPI가 Gemini SDK를 호출하고,
    질문/답변/처리 상태를 `simple_chat_logs` 테이블에 저장합니다.

    01_insert_conversation_and_log.py가 "샘플 로그 저장"만 확인했다면,
    이 파일은 실제 API endpoint에서 LLM 응답과 DB 저장을 연결합니다.

    `simple_chat_logs`에는 user_id를 넣지 않습니다.
    이 예제의 `/chat` endpoint는 아직 Authorization 헤더로 로그인 사용자를 확인하지 않습니다.
    사용자별 로그 저장은 Auth/JWT를 연결한 뒤 user_id 컬럼을 추가하는 방식으로 확장합니다.

실행 전 준비:
    1. C:/aidevs/02_supabase-ai-backend/.env 파일에 아래 값이 있어야 합니다.
       - SUPABASE_URL
       - SUPABASE_SERVICE_ROLE_KEY
       - GEMINI_API_KEY
       - GEMINI_MODEL

    2. Supabase SQL Editor에서 아래 SQL을 실행해 simple_chat_logs 테이블을 만듭니다.

       create table if not exists simple_chat_logs (
         id uuid primary key default gen_random_uuid(),
         user_message text not null,
         assistant_message text,
         provider text not null default 'gemini',
         model text,
         status text not null default 'success',
         error_message text,
         created_at timestamptz not null default now()
       );

실행:
    cd C:/aidevs/02_supabase-ai-backend/03_supabase-db-and-auth/05_conversation-history-and-service-logs
    ../../.venv/Scripts/Activate.ps1
    uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003

Swagger 확인:
    http://127.0.0.1:8003/docs

Swagger에서 확인할 endpoint:
    - GET  /health : FastAPI 서버 실행 확인
    - POST /chat   : Gemini 답변 생성 + Supabase 로그 저장
    - GET  /logs   : 최근 채팅 로그 조회
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from supabase import Client, create_client


# .env 파일은 02_supabase-ai-backend 폴더에 있습니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

# 앱이 import될 때 .env를 한 번 읽어 둡니다.
load_dotenv(ENV_PATH)

app = FastAPI(
    title="FastAPI LLM Chat Log",
    description="Gemini 답변을 생성하고 simple_chat_logs 테이블에 저장하는 예제입니다.",
)


class ChatRequest(BaseModel):
    """Swagger에서 사용자가 보낼 질문 구조입니다."""

    message: str = Field(
        min_length=1,
        max_length=500,
        examples=["Supabase와 Redis는 언제 나눠서 사용하나요?"],
        description="LLM에게 보낼 사용자 질문입니다.",
    )


class ChatResponse(BaseModel):
    """POST /chat 응답 구조입니다.

    answer:
        Gemini가 생성한 답변입니다.

    log_id:
        simple_chat_logs 테이블에 저장된 로그 id입니다.
        나중에 Supabase Table Editor에서 같은 id를 찾아볼 수 있습니다.
    """

    answer: str
    log_id: str | None = None
    provider: str
    model: str
    status: str


class ChatLogItem(BaseModel):
    """GET /logs 응답에서 보여 줄 로그 1건의 구조입니다."""

    id: str
    user_message: str
    assistant_message: str | None = None
    provider: str
    model: str | None = None
    status: str
    error_message: str | None = None
    created_at: str


def get_supabase() -> Client:
    """로그 저장에 사용할 Supabase client를 만듭니다.

    이 예제는 FastAPI 서버가 DB에 로그를 저장하는 흐름입니다.
    따라서 서버 전용 `SUPABASE_SERVICE_ROLE_KEY`를 사용합니다.

    주의:
    service role key는 프론트엔드나 GitHub에 노출하면 안 됩니다.
    """

    url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url:
        raise HTTPException(500, "SUPABASE_URL이 없습니다. .env 파일을 확인하세요.")

    if not service_role_key:
        raise HTTPException(500, "SUPABASE_SERVICE_ROLE_KEY가 없습니다. .env 파일을 확인하세요.")

    return create_client(url, service_role_key)


def create_gemini_answer(message: str) -> tuple[str, str]:
    """Gemini SDK로 답변을 생성합니다.

    입력:
        message: 사용자가 Swagger에서 보낸 질문

    반환:
        (answer, model)
        answer는 Gemini가 생성한 답변이고, model은 사용한 모델 이름입니다.
    """

    # .env를 load_dotenv()로 읽었으므로 os.getenv()에서 값을 가져올 수 있습니다.
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(500, "GEMINI_API_KEY가 없습니다. .env 파일을 확인하세요.")

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    from google import genai
    client = genai.Client(api_key=api_key)

    # Gemini에게 보낼 최종 프롬프트입니다.
    # 사용자의 질문만 그대로 보내기보다, "초보자에게 짧고 명확하게 답하라"는 역할을 같이 전달합니다.
    prompt = (
        "당신은 Python, FastAPI, Supabase를 쉽게 설명하는 학습 도우미입니다.\n"
        "초보자가 이해할 수 있도록 짧고 명확하게 답하세요.\n\n"
        f"사용자 질문:\n{message}"
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        # config={
        #     "temperature": 0.3,
        #     "max_output_tokens": 300,
        # },
    )

    return response.text or "", model


def save_chat_log(
    supabase: Client,
    user_message: str,
    assistant_message: str | None,
    provider: str,
    model: str,
    status_value: str,
    error_message: str | None = None,
) -> dict:
    """LLM 처리 결과를 simple_chat_logs 테이블에 저장합니다.

    성공했을 때:
        user_message, assistant_message, status='success'를 저장합니다.

    실패했을 때:
        user_message, status='error', error_message를 저장합니다.
    """

    result = (
        supabase.table("simple_chat_logs")
        .insert(
            {
                "user_message": user_message,
                "assistant_message": assistant_message,
                "provider": provider,
                "model": model,
                "status": status_value,
                "error_message": error_message,
            }
        )
        .execute()
    )

    return result.data[0]


@app.get("/health")
def health_check() -> dict[str, str | bool]:
    """서버 실행과 .env 설정 여부를 확인합니다."""

    return {
        "status": "ok",
        "supabase_configured": bool(os.getenv("SUPABASE_URL")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """사용자 질문을 Gemini에 보내고, 질문/답변을 Supabase에 저장합니다."""

    provider = "gemini"
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    # 1. .env 설정을 읽고 Gemini 답변을 만듭니다.
    supabase = get_supabase()
    answer, model = create_gemini_answer(request.message)

    # 3. 질문과 답변을 Supabase에 저장합니다.
    saved_log = save_chat_log(
        supabase=supabase,
        user_message=request.message,
        assistant_message=answer,
        provider=provider,
        model=model,
        status_value="success",
    )

    return ChatResponse(
        answer=answer,
        log_id=saved_log["id"],
        provider=provider,
        model=model,
        status="success",
    )


@app.get("/logs", response_model=list[ChatLogItem])
def list_logs(limit: int = 10) -> list[dict]:
    """최근 채팅 로그를 조회합니다."""

    supabase = get_supabase()

    # limit 값이 너무 작거나 너무 크지 않도록 조정합니다.
    # 예: /logs?limit=1000 같은 요청으로 너무 많은 데이터를 가져오지 않게 합니다.
    safe_limit = max(1, min(limit, 50))

    result = (
        supabase.table("simple_chat_logs")
        .select("*")
        .order("created_at", desc=True)
        .limit(safe_limit)
        .execute()
    )

    return result.data
