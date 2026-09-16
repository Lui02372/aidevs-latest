"""Notes API의 시작 파일입니다. 실행: python -m uvicorn app.main:app --reload --port 8011"""

from fastapi import FastAPI

from app.routers.notes_router import router as notes_router


app = FastAPI(
    title="Notes API With Supabase",
    description="초보자를 위한 노트 CRUD 미니 프로젝트",
    version="1.0.0",
)
app.include_router(notes_router)
