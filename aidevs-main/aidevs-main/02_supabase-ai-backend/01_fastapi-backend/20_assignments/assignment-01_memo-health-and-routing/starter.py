"""Assignment 01 starter: 메모 상태 확인과 라우팅 과제.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from typing import Any

from fastapi import FastAPI, HTTPException, Query


app = FastAPI(title="Assignment 01 Memo Routing")


memos: dict[int, dict[str, Any]] = {
    1: {"id": 1, "title": "FastAPI 시작", "content": "서버 실행과 라우팅을 복습합니다."},
    2: {"id": 2, "title": "메모 검색", "content": "Query Parameter로 검색어를 받습니다."},
}


@app.get("/health")
def health_check():
    """TODO: 서버 상태를 반환하세요."""

    return {"status": "TODO"}


@app.get("/memos")
def list_memos():
    """TODO: 전체 메모 목록과 개수를 반환하세요."""

    return {"count": "TODO", "data": "TODO"}


@app.get("/memos/search")
def search_memos(
    keyword: str = Query(default="", description="검색어입니다."),
    limit: int = Query(default=10, ge=1, le=20, description="최대 결과 개수입니다."),
):
    """TODO: 제목 또는 본문에 keyword가 포함된 메모를 반환하세요."""

    return {"keyword": keyword, "limit": limit, "data": "TODO"}


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int):
    """TODO: 메모 1개를 반환하고, 없으면 404 오류를 반환하세요."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return {"data": "TODO"}
