r"""01_realtime-log-dashboard-practice backend.

실행:
    cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\backend
    C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME, CORS_ALLOW_ORIGINS
from app.routers.log_router import router as log_router
from app.services.db_service import storage_status
from app.services.event_service import event_status


# FastAPI 애플리케이션 객체입니다.
# uvicorn은 "app.main:app" 경로를 보고 이 객체를 찾아 실행합니다.
app = FastAPI(title=APP_NAME)

# Streamlit frontend는 보통 8501 포트, FastAPI backend는 8000 포트에서 실행됩니다.
# 포트가 다르면 브라우저 기준 origin이 다르므로 CORS 허용이 필요합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 로그 생성/조회/SSE endpoint를 제공하는 router를 등록합니다.
app.include_router(log_router)


@app.get("/health")
def health() -> dict:
    """backend 실행 상태와 Supabase/Upstash Redis 설정 여부를 확인합니다."""

    storage = storage_status()
    event = event_status()

    return {
        "status": "ok",
        "supabase_configured": storage["supabase_configured"],
        "redis_configured": event["redis_configured"],
        "expected_storage_mode": storage["expected_storage_mode"],
        "last_storage_mode": storage["last_storage_mode"],
        "last_storage_error": storage["last_storage_error"],
        "expected_event_mode": event["expected_event_mode"],
        "last_event_mode": event["last_event_mode"],
        "last_event_error": event["last_event_error"],
        "message": "04 mini project realtime backend is running",
    }
