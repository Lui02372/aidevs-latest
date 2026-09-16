r"""Auth JWT Profile API 구조화 예제입니다.

실행:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\04_auth-jwt-profile-api
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8014
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8014
"""

from fastapi import FastAPI

from app.routers.auth_router import router as auth_router
from app.routers.profile_router import router as profile_router


# Auth router는 회원가입/로그인/token 확인을 담당합니다.
# Profile router는 로그인한 사용자의 프로필 조회/저장을 담당합니다.
app = FastAPI(title="Example 04 - Auth JWT Profile API")
app.include_router(auth_router)
app.include_router(profile_router)
