r"""03_project_structure backend starter.

실행:
    cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\backend
    C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

이 파일은 학생들이 프로젝트를 시작할 수 있도록 health endpoint만 제공합니다.
로그 API, 피드백 API, SSE endpoint는 routers 폴더에 직접 구현합니다.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME, CORS_ALLOW_ORIGINS, is_redis_configured, is_supabase_configured


# FastAPI 애플리케이션 객체입니다.
# 학생들은 이 객체에 router를 추가하면서 프로젝트를 확장합니다.
app = FastAPI(title=APP_NAME)

# Streamlit frontend와 FastAPI backend가 다른 포트에서 실행되므로 CORS가 필요합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO:
# 1. app.routers.log_router를 만들고 app.include_router(log_router)를 추가합니다.
# 2. app.routers.feedback_router를 만들고 app.include_router(feedback_router)를 추가합니다.
# 3. app.routers.stream_router 또는 log_router 안에 /stream/logs SSE endpoint를 추가합니다.
# 4. 구현 예시는 01_realtime-log-dashboard-practice/backend/app 폴더를 참고합니다.


@app.get("/health")
def health() -> dict:
    """starter backend가 정상 실행되는지 확인하는 최소 API입니다."""

    return {
        "status": "ok",
        "supabase_configured": is_supabase_configured(),
        "redis_configured": is_redis_configured(),
        "message": "04 mini project starter backend is running",
    }
