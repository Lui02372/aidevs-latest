"""Lab 03 starter: 메모 요청 Body 검증.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from fastapi import FastAPI, status
from pydantic import BaseModel, Field


app = FastAPI(title="Memo Request Validation Lab Starter")


class MemoCreate(BaseModel):
    """TODO: 메모 생성 요청 모델을 완성해 보세요."""

    title: str = Field(min_length=1)
    # TODO: content 필드를 추가하고 1~500자로 제한해 보세요.
    # TODO: tags 필드를 추가하고 기본값은 빈 목록, 최대 5개로 제한해 보세요.


@app.post("/memos", status_code=status.HTTP_201_CREATED)
def create_memo(memo: MemoCreate):
    """TODO: 검증된 메모 데이터를 응답으로 반환해 보세요."""

    return {
        "message": "TODO",
        "data": "TODO",
    }
