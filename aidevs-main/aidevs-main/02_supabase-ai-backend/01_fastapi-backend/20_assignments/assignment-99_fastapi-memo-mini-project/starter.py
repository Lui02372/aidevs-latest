"""Assignment 99 starter: FastAPI 메모 미니 프로젝트.

이 파일은 시작용 뼈대입니다. 완성한 코드는 main.py로 정리해 제출합니다.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

import asyncio
from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


app = FastAPI(title="FastAPI Memo Mini Project Starter")


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None


class MemoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


class MemoUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


class MemoPublic(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]


class ChatDraftRequest(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    tone: str = Field(default="friendly", max_length=30)


memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "FastAPI 마무리",
        "content": "메모 API 미니 프로젝트를 완성합니다.",
        "tags": ["fastapi", "memo"],
        "internal_note": "응답으로 내보내면 안 되는 내부 관리 값입니다.",
    }
}
next_memo_id = 2


@app.get("/health")
def health_check():
    """TODO: 서버 상태를 반환하세요."""

    return {"status": "TODO"}


@app.get("/memos", response_model=ApiResponse)
def list_memos():
    """TODO: 전체 메모를 표준 응답 구조로 반환하세요."""

    return ApiResponse(success=True, message="TODO", data="TODO")


@app.get("/memos/search", response_model=ApiResponse)
def search_memos(keyword: str = "", limit: int = Query(default=10, ge=1, le=20)):
    """TODO: 제목 또는 본문 검색을 구현하세요."""

    return ApiResponse(success=True, message="TODO", data="TODO")


@app.get("/memos/{memo_id}", response_model=MemoPublic)
def get_memo(memo_id: int):
    """TODO: 메모 1개를 조회하고 없는 id는 404를 반환하세요."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return memos[memo_id]


@app.post("/memos", response_model=MemoPublic, status_code=status.HTTP_201_CREATED)
def create_memo(memo: MemoCreate):
    """TODO: 새 메모를 생성하세요."""

    return {
        "id": 0,
        "title": memo.title,
        "content": memo.content,
        "tags": memo.tags,
        "internal_note": "TODO",
    }


@app.put("/memos/{memo_id}", response_model=MemoPublic)
def update_memo(memo_id: int, memo: MemoUpdate):
    """TODO: 기존 메모를 수정하세요."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return memos[memo_id]


@app.delete("/memos/{memo_id}", response_model=ApiResponse)
def delete_memo(memo_id: int):
    """TODO: 기존 메모를 삭제하세요."""

    return ApiResponse(success=True, message="TODO", data={"deleted_id": memo_id})


@app.post("/ai/draft-response", response_model=ApiResponse)
async def create_ai_draft_response(request: ChatDraftRequest):
    """TODO: 실제 LLM API 전 가짜 AI 응답을 비동기로 반환하세요."""

    await asyncio.sleep(1)
    return ApiResponse(success=True, message="TODO", data="TODO")
