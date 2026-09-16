"""Lab 99 solution: 작은 메모 API 서버 완성하기.

??:
    uvicorn solution:app --reload

? ???? ??? ??:
    python -m uvicorn solution:app --reload
"""

import asyncio
from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


app = FastAPI(title="Mini Memo API Server")


class MemoCreate(BaseModel):
    """메모 생성 요청 모델입니다."""

    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=5)


class MemoPublic(BaseModel):
    """외부 응답에 공개할 메모 모델입니다."""

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
    """서버 상태를 반환합니다."""

    return {"status": "ok"}


@app.get("/memos")
def list_memos():
    """전체 메모를 반환하되 internal_note는 제외합니다."""

    public_memos = [MemoPublic(**memo).model_dump() for memo in memos.values()]
    return {"count": len(public_memos), "data": public_memos}


@app.get("/memos/search")
def search_memos(keyword: str = "", limit: int = Query(default=10, ge=1, le=20)):
    """제목 또는 본문에 검색어가 포함된 메모를 반환합니다."""

    normalized_keyword = keyword.lower()
    result = [
        MemoPublic(**memo).model_dump()
        for memo in memos.values()
        if normalized_keyword in memo["title"].lower()
        or normalized_keyword in memo["content"].lower()
    ]

    return {"keyword": keyword, "limit": limit, "count": len(result[:limit]), "data": result[:limit]}


@app.get("/memos/{memo_id}", response_model=MemoPublic)
def get_memo(memo_id: int):
    """메모 1개를 조회합니다."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return memos[memo_id]


@app.post("/memos", status_code=status.HTTP_201_CREATED, response_model=MemoPublic)
def create_memo(memo: MemoCreate):
    """새 메모를 생성합니다."""

    global next_memo_id

    new_memo = {
        "id": next_memo_id,
        "title": memo.title,
        "content": memo.content,
        "tags": memo.tags,
        "internal_note": "새 메모의 내부 관리 값입니다.",
    }
    memos[next_memo_id] = new_memo
    next_memo_id += 1

    return new_memo


@app.post("/ai/draft-response")
async def create_ai_draft_response(request: ChatDraftRequest):
    """실제 LLM API 연결 전 비동기 응답 흐름을 확인합니다."""

    await asyncio.sleep(1)

    return {
        "message": "draft response generated",
        "data": {
            "question": request.question,
            "answer": f"[{request.tone}] '{request.question}'에 대한 샘플 답변입니다.",
        },
    }
