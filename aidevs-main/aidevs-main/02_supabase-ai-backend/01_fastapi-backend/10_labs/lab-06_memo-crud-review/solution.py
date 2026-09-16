"""Lab 06 solution: 메모 CRUD 복습.

??:
    uvicorn solution:app --reload

? ???? ??? ??:
    python -m uvicorn solution:app --reload
"""

from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Memo CRUD Review")


class MemoCreate(BaseModel):
    """메모 생성 요청 모델입니다."""

    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


class MemoUpdate(BaseModel):
    """메모 수정 요청 모델입니다."""

    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


memos: dict[int, dict[str, Any]] = {
    1: {"id": 1, "title": "FastAPI CRUD", "content": "메모 CRUD를 복습합니다.", "tags": ["crud"]}
}
next_memo_id = 2


@app.get("/memos")
def list_memos():
    """전체 메모 목록과 개수를 반환합니다."""

    memo_list = list(memos.values())
    return {"count": len(memo_list), "data": memo_list}


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int):
    """메모 1개를 조회합니다."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return {"data": memos[memo_id]}


@app.post("/memos", status_code=status.HTTP_201_CREATED)
def create_memo(memo: MemoCreate):
    """새 메모를 생성합니다."""

    global next_memo_id

    new_memo = {
        "id": next_memo_id,
        "title": memo.title,
        "content": memo.content,
        "tags": memo.tags,
    }
    memos[next_memo_id] = new_memo
    next_memo_id += 1

    return {"message": "memo created", "data": new_memo}


@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, memo: MemoUpdate):
    """기존 메모를 수정합니다."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    updated_memo = {
        "id": memo_id,
        "title": memo.title,
        "content": memo.content,
        "tags": memo.tags,
    }
    memos[memo_id] = updated_memo

    return {"message": "memo updated", "data": updated_memo}


@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    """기존 메모를 삭제합니다."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    del memos[memo_id]

    return {"message": "memo deleted", "deleted_id": memo_id}
