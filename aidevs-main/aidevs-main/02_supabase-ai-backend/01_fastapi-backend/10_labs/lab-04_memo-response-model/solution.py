"""Lab 04 solution: 메모 응답 모델.

??:
    uvicorn solution:app --reload

? ???? ??? ??:
    python -m uvicorn solution:app --reload
"""

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Memo Response Model Lab")


class MemoPublic(BaseModel):
    """외부에 공개해도 되는 메모 응답 모델입니다."""

    id: int
    title: str
    content: str
    tags: list[str]


memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "응답 모델 연습",
        "content": "internal_note가 응답에서 제외되는지 확인합니다.",
        "tags": ["response"],
        "internal_note": "응답으로 내보내면 안 되는 내부 관리 값입니다.",
    }
}


@app.get("/memos/{memo_id}", response_model=MemoPublic)
def get_memo(memo_id: int):
    """메모를 조회하되 내부 관리 값은 응답에서 제외합니다."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return memos[memo_id]
