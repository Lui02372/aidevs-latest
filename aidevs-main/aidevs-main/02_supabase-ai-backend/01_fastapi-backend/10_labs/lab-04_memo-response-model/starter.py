"""Lab 04 starter: 메모 응답 모델.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Memo Response Model Lab Starter")


class MemoPublic(BaseModel):
    """TODO: 외부에 공개할 메모 응답 모델을 완성해 보세요."""

    id: int
    title: str
    # TODO: content와 tags 필드를 추가해 보세요.


memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "응답 모델 연습",
        "content": "internal_note가 응답에서 제외되는지 확인합니다.",
        "tags": ["response"],
        "internal_note": "응답으로 내보내면 안 되는 내부 관리 값입니다.",
    }
}


@app.get("/memos/{memo_id}")  # TODO: response_model=MemoPublic을 추가해 보세요.
def get_memo(memo_id: int):
    """TODO: 메모를 조회하고 없는 id는 404를 반환해 보세요."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return memos[memo_id]
