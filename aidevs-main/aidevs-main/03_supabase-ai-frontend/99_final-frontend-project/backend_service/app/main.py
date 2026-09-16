r"""99_final-frontend-project 실제 서비스 연결용 backend입니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service
    C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

이 backend는 Supabase Auth, Supabase DB, Gemini API를 사용합니다.
Upstash Redis는 같은 질문에 대한 응답을 캐시하는 선택 확장입니다.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME, CORS_ALLOW_ORIGINS
from app.routers.auth_router import router as auth_router
from app.routers.chat_router import router as chat_router
from app.routers.log_router import router as log_router


# FastAPI 애플리케이션 객체입니다.
# uvicorn은 "app.main:app" 경로를 보고 이 객체를 찾아 서버로 실행합니다.
app = FastAPI(title=APP_NAME)

# Streamlit 프론트엔드와 FastAPI 백엔드가 다른 포트에서 실행되므로 CORS 설정이 필요합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기능별 router를 앱에 등록합니다.
# auth_router: Supabase Auth, chat_router: Gemini/DB, log_router: 운영 로그
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(log_router)


@app.get("/health")
def health() -> dict[str, str]:
    """외부 서비스 연결 없이 백엔드 서버 실행 상태만 확인하는 API입니다."""

    return {
        "status": "ok",
        "mode": "supabase-gemini-upstash-optional",
        "message": "99 final frontend project service backend is running",
    }
