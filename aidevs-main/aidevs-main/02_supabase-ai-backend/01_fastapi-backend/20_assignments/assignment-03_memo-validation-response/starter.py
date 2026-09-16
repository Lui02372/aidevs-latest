"""Assignment 03 starter: 메모 요청 검증과 응답 모델 과제.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Assignment 03 Memo Validation Response")


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None


class MemoCreate(BaseModel):
    """TODO: 요청 검증 조건을 완성하세요."""

    title: str = Field(min_length=1)
    # TODO: content, tags 필드를 추가하세요.


class MemoPublic(BaseModel):
    """TODO: 외부 응답에 공개할 필드를 정의하세요."""

    id: int
    title: str
    # TODO: content, tags 필드를 추가하세요.


memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "응답 모델",
        "content": "internal_note가 응답에서 제외되는지 확인합니다.",
        "tags": ["response"],
        "internal_note": "응답으로 내보내면 안 되는 내부 관리 값입니다.",
    }
}
next_memo_id = 2


@app.post("/memos", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_memo(memo: MemoCreate):
    """TODO: 새 메모를 만들고 표준 응답 구조로 반환하세요."""

    return ApiResponse(success=True, message="TODO", data="TODO")


@app.get("/memos/{memo_id}")  # TODO: response_model=MemoPublic을 추가하세요.
def get_memo(memo_id: int):
    """TODO: 메모를 조회하고 internal_note가 응답에서 제외되도록 하세요."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return memos[memo_id]
