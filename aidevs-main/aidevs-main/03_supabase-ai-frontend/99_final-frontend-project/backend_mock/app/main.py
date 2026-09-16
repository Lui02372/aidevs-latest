r"""99_final-frontend-project 프론트 개발용 mock backend입니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_mock
    C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
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

# Streamlit은 보통 8501 포트, FastAPI는 8000 포트에서 실행됩니다.
# 브라우저는 서로 다른 포트의 요청을 다른 origin으로 보기 때문에 CORS 허용이 필요합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기능별 router를 앱에 등록합니다.
# auth_router: 회원가입/로그인, chat_router: 채팅, log_router: 서비스 로그
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(log_router)


@app.get("/health")
def health() -> dict[str, str]:
    """프론트엔드나 배포 환경에서 백엔드가 켜져 있는지 확인하는 API입니다."""

    return {
        "status": "ok",
        "mode": "mock-memory",
        "message": "99 final frontend project backend is running",
    }
