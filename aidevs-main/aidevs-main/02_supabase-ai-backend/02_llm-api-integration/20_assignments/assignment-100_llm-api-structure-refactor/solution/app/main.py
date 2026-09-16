r"""LLM API 구조 분리 과제의 solution 실행 시작점입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\20_assignments\assignment-100_llm-api-structure-refactor\solution
    uvicorn app.main:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.routers.chat_router import router as chat_router


app = FastAPI(title="LLM API Structure Refactor Solution")
app.include_router(chat_router)
