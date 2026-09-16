"""Redis multi-turn chat API 실행 파일입니다."""

from fastapi import FastAPI

from app.routers.chat_router import router as chat_router


app = FastAPI(title="Example 02 - Simple Multi-turn Redis Chat API")
app.include_router(chat_router)
