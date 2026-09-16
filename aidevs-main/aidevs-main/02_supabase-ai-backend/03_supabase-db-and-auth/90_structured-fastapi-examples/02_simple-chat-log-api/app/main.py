r"""Simple Chat Log API 구조화 예제입니다.

실행:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\02_simple-chat-log-api
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8012
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8012
"""

from fastapi import FastAPI

from app.routers.chat_router import router as chat_router


# main.py는 앱을 생성하고 router를 연결하는 입구 역할만 합니다.
# 실제 /chat, /logs 코드는 app/routers/chat_router.py에 있습니다.
app = FastAPI(title="Example 02 - Simple Chat Log API")
app.include_router(chat_router)
