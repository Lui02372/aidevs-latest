r"""Cached AI Answer API 구조화 예제입니다.

실행:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\03_cached-ai-answer-api
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8013
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8013
"""

from fastapi import FastAPI

from app.routers.cache_router import router as cache_router


# Redis 캐시 예제의 FastAPI 앱입니다.
# endpoint 정의는 app/routers/cache_router.py에서 관리합니다.
app = FastAPI(title="Example 03 - Cached AI Answer API")
app.include_router(cache_router)
