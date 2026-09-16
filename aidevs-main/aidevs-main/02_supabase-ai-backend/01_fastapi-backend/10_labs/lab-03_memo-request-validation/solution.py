"""Lab 03 solution: 메모 요청 Body 검증.

??:
    uvicorn solution:app --reload

? ???? ??? ??:
    python -m uvicorn solution:app --reload
"""

from fastapi import FastAPI, status
from pydantic import BaseModel, Field


app = FastAPI(title="Memo Request Validation Lab")


class MemoCreate(BaseModel):
    """메모 생성 요청 데이터입니다."""

    title: str = Field(min_length=1, max_length=50, examples=["FastAPI 복습"])
    content: str = Field(min_length=1, max_length=500, examples=["요청 검증을 연습합니다."])
    tags: list[str] = Field(default_factory=list, max_length=5, examples=[["fastapi", "pydantic"]])


@app.post("/memos", status_code=status.HTTP_201_CREATED)
def create_memo(memo: MemoCreate):
    """검증된 메모 데이터를 응답으로 반환합니다."""

    return {
        "message": "memo data is valid",
        "data": memo.model_dump(),
    }
