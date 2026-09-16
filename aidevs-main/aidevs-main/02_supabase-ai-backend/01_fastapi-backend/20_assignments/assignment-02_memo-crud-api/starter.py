"""Assignment 02 starter: 메모 CRUD API 과제.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Assignment 02 Memo CRUD")


class MemoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


class MemoUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


memos: dict[int, dict[str, Any]] = {
    1: {"id": 1, "title": "FastAPI CRUD", "content": "메모 CRUD를 구현합니다.", "tags": ["crud"]}
}
next_memo_id = 2


@app.get("/memos")
def list_memos():
    """TODO: 전체 메모를 반환하세요."""

    return {"count": "TODO", "data": "TODO"}


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int):
    """TODO: 메모 1개를 반환하세요."""

    return {"data": "TODO"}


@app.post("/memos", status_code=status.HTTP_201_CREATED)
def create_memo(memo: MemoCreate):
    """TODO: 새 메모를 생성하세요."""

    return {"message": "TODO", "data": "TODO"}


@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, memo: MemoUpdate):
    """TODO: 기존 메모를 수정하세요."""

    return {"message": "TODO", "data": "TODO"}


@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    """TODO: 기존 메모를 삭제하세요."""

    return {"message": "TODO"}
