"""Lab 99 starter: 작은 메모 API 서버 완성하기.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

import asyncio
from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


app = FastAPI(title="Mini Memo API Server Starter")


class MemoCreate(BaseModel):
    """TODO: 메모 생성 요청 모델을 완성해 보세요."""

    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


class MemoPublic(BaseModel):
    """TODO: 외부 응답에 공개할 메모 모델을 완성해 보세요."""

    id: int
    title: str
    content: str
    tags: list[str]


class ChatDraftRequest(BaseModel):
    """AI 응답 초안 요청 모델입니다."""

    question: str = Field(min_length=1, max_length=300)
    tone: str = Field(default="friendly", max_length=30)


memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "FastAPI 마무리",
        "content": "메모 API 서버를 완성합니다.",
        "tags": ["fastapi", "memo"],
        "internal_note": "응답으로 내보내지 않을 내부 관리 값입니다.",
    }
}
next_memo_id = 2


@app.get("/health")
def health_check():
    """TODO: 서버 상태를 반환해 보세요."""

    return {"status": "TODO"}


@app.get("/memos")
def list_memos():
    """TODO: 전체 메모를 반환하되 internal_note는 제외해 보세요."""

    return {"count": "TODO", "data": "TODO"}


@app.get("/memos/search")
def search_memos(keyword: str = "", limit: int = Query(default=10, ge=1, le=20)):
    """TODO: 제목 또는 본문 검색을 구현해 보세요."""

    return {"keyword": keyword, "limit": limit, "data": "TODO"}


@app.get("/memos/{memo_id}", response_model=MemoPublic)
def get_memo(memo_id: int):
    """TODO: 메모 1개를 조회하고 없는 id는 404를 반환해 보세요."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return memos[memo_id]


@app.post("/memos", status_code=status.HTTP_201_CREATED, response_model=MemoPublic)
def create_memo(memo: MemoCreate):
    """TODO: 새 메모를 생성해 보세요."""

    return {
        "id": 0,
        "title": memo.title,
        "content": memo.content,
        "tags": memo.tags,
        "internal_note": "TODO",
    }


@app.post("/ai/draft-response")
async def create_ai_draft_response(request: ChatDraftRequest):
    """TODO: 가짜 AI 응답을 비동기로 반환해 보세요."""

    await asyncio.sleep(1)
    return {"message": "TODO"}
