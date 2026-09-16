r"""05_ai-chatbot-interface 전용 FastAPI 챗봇 샘플 백엔드입니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    cd .\05_ai-chatbot-interface\00_sample_backend
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

위 명령에서 uvicorn 실행이 막히거나 오류가 나면:
    python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

실행 확인:
    http://127.0.0.1:8000/health
    http://127.0.0.1:8000/docs

이 파일은 Streamlit 챗봇 화면이 호출할 백엔드 API를 제공합니다.
Streamlit 프론트엔드는 API_BASE_URL만 알고, Gemini API key는 이 백엔드 폴더의 .env에만 둡니다.
"""

from pathlib import Path  # 현재 파일 기준으로 .env 위치를 안전하게 찾기 위해 사용합니다.

from dotenv import dotenv_values  # 백엔드 전용 .env 파일의 값을 dict로 읽습니다.
from fastapi import FastAPI, HTTPException, status  # API 앱, 오류 응답, HTTP 상태 코드를 사용합니다.
from fastapi.middleware.cors import CORSMiddleware  # Streamlit 화면에서 백엔드를 호출할 수 있도록 CORS를 설정합니다.
from pydantic import BaseModel, Field  # 요청/응답 JSON 구조와 검증 규칙을 정의합니다.


# 이 .env는 프론트엔드용이 아니라 04 챗봇 샘플 백엔드용입니다.
# 즉, C:\aidev\03_supabase-ai-frontend\.env가 아니라
# C:\aidev\03_supabase-ai-frontend\05_ai-chatbot-interface\00_sample_backend\.env를 읽습니다.
BACKEND_ENV_PATH = Path(__file__).resolve().parent / ".env"
BACKEND_ENV = dotenv_values(BACKEND_ENV_PATH)

GEMINI_MODEL = str(BACKEND_ENV.get("GEMINI_MODEL") or "gemini-2.5-flash-lite").strip()


app = FastAPI(title="Chatbot Interface Sample Backend")

# Streamlit은 보통 http://localhost:8501에서 실행되고,
# FastAPI는 http://127.0.0.1:8000에서 실행됩니다.
# 브라우저 입장에서는 포트가 다르면 다른 출처(origin)이므로 CORS 허용이 필요합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    """Streamlit 화면에서 백엔드로 함께 보낼 수 있는 이전 대화 메시지 구조입니다."""

    role: str = Field(..., description="메시지 역할입니다. 예: user 또는 assistant")
    content: str = Field(..., min_length=1, description="메시지 내용입니다.")


class ChatRequest(BaseModel):
    """Streamlit 챗봇 화면에서 백엔드로 보내는 요청 JSON 구조입니다."""

    question: str = Field(..., min_length=1, description="사용자가 입력한 질문")
    messages: list[ChatMessage] = Field(
        default_factory=list,
        description="선택 사항입니다. 문맥 유지를 위해 함께 보낼 최근 대화 메시지 목록입니다.",
    )


class ChatResponse(BaseModel):
    """백엔드가 Streamlit 챗봇 화면으로 돌려주는 응답 JSON 구조입니다."""

    answer: str
    provider: str
    model: str
    actual_api_called: bool


def print_api_running(method: str, path: str):
    """현재 실행된 API URL 정보를 FastAPI 터미널에 출력합니다."""

    base_url = "http://127.0.0.1:8000"
    print(f"[chat api running] {method} {base_url}{path}")


def print_client_request(api_name: str, payload: BaseModel):
    """Streamlit 화면에서 백엔드로 보낸 요청 데이터를 터미널에 출력합니다."""

    request_data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()

    print("\n" + "=" * 60)
    print(f"[chat client request] {api_name}")
    print("Streamlit 화면에서 전송한 데이터:")

    for key, value in request_data.items():
        print(f"- {key}: {value}")

    print("=" * 60)


def read_gemini_api_key():
    """백엔드 전용 .env에서 GEMINI_API_KEY를 읽고 검증합니다."""

    # 의도적으로 OS 전역 환경변수는 읽지 않습니다.
    # 이 예제에서는 수강생이 "04 챗봇 백엔드 폴더의 .env"에 key를 둔다는 기준을 명확히 하기 위해
    # dotenv_values()로 읽은 BACKEND_ENV dict만 사용합니다.
    api_key = str(BACKEND_ENV.get("GEMINI_API_KEY") or "").strip()

    if not api_key or api_key.startswith("your-"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "GEMINI_API_KEY가 설정되어 있지 않습니다. "
                "05_ai-chatbot-interface/00_sample_backend/.env 파일을 확인하세요."
            ),
        )

    return api_key


def build_prompt_with_history(request: ChatRequest):
    """이전 대화와 현재 질문을 Gemini에 보낼 하나의 프롬프트로 합칩니다."""

    # 08 예제에서는 최근 6개 메시지만 백엔드로 보냅니다.
    # 백엔드는 전달받은 메시지를 그대로 이어 붙여 Gemini가 앞 대화를 참고할 수 있게 합니다.
    # 실제 서비스에서는 더 많은 메시지를 함께 보내거나, 오래된 대화는 요약해서 보내거나,
    # DB/Vector DB에서 필요한 기억만 검색해 함께 보내는 방식으로 확장할 수 있습니다.
    if not request.messages:
        return request.question

    history_lines = []

    for message in request.messages:
        history_lines.append(f"{message.role}: {message.content}")

    history_text = "\n".join(history_lines)

    return (
        "아래는 지금까지의 대화입니다.\n"
        f"{history_text}\n\n"
        "위 대화의 문맥을 참고해서 현재 질문에 답하세요.\n"
        f"현재 질문: {request.question}"
    )


@app.get("/")
def read_root():
    """브라우저에서 루트 주소를 열었을 때 서버 상태를 확인하는 API입니다."""

    print_api_running("GET", "/")
    return {"message": "Chatbot Interface Sample Backend is running"}


@app.get("/health")
def health_check():
    """Streamlit 화면이 챗봇 백엔드 실행 여부를 확인할 때 사용하는 API입니다."""

    print_api_running("GET", "/health")
    return {
        "status": "ok",
        "service": "chatbot-interface-sample-backend",
    }


@app.post("/api/chat/mock", response_model=ChatResponse)
def create_mock_chat(request: ChatRequest):
    """비용 없이 챗봇 화면을 테스트하기 위한 mock 응답 API입니다."""

    print_api_running("POST", "/api/chat/mock")
    print_client_request("/api/chat/mock", request)
    if request.question == "폭탄":
        raise HTTPException(
            status_code=409,
            detail="mock API는 '폭탄'이라는 메시지를 처리할 수 없습니다.",
        )
       
    return ChatResponse(
        answer=f"'{request.question}'에 대한 mock 응답입니다. 함께 받은 이전 메시지 수: {len(request.messages)}개",
        provider="mock",
        model="mock-chat",
        actual_api_called=False,
    )


@app.post("/api/chat/gemini", response_model=ChatResponse)
def create_gemini_chat(request: ChatRequest):
    """Gemini API를 백엔드에서 호출하고 Streamlit 화면에 응답을 돌려주는 API입니다."""

    print_api_running("POST", "/api/chat/gemini")
    print_client_request("/api/chat/gemini", request)

    api_key = read_gemini_api_key()

    try:
        from google import genai  # google-genai 패키지는 실제 Gemini 호출이 필요할 때만 가져옵니다.

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=build_prompt_with_history(request),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gemini API 호출에 실패했습니다: {exc}",
        ) from exc

    answer = getattr(response, "text", "") or "Gemini 응답이 비어 있습니다."

    return ChatResponse(
        answer=answer,
        provider="gemini",
        model=GEMINI_MODEL,
        actual_api_called=True,
    )
