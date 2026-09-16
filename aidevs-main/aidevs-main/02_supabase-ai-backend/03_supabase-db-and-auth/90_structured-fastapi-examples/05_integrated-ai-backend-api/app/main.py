r"""Integrated AI Backend API 구조화 예제입니다.

실행:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\05_integrated-ai-backend-api
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8015
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8015
"""

from fastapi import FastAPI

from app.routers.auth_router import router as auth_router
from app.routers.chat_router import router as chat_router


# 통합 예제의 앱 시작점입니다.
# auth_router는 로그인/token 확인, chat_router는 AI 답변/캐시/로그 조회를 담당합니다.
app = FastAPI(title="Example 05 - Integrated AI Backend API")
app.include_router(auth_router)
app.include_router(chat_router)
