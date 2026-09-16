from fastapi import FastAPI

from app.routers.memo_router import router as memo_router


app = FastAPI(title="Mini Memo API - Structured Starter")
app.include_router(memo_router)
