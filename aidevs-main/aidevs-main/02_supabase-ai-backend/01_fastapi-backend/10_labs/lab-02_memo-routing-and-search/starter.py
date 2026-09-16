"""Lab 02 starter: 메모 라우팅과 검색.

Path Parameter와 Query Parameter를 사용해 메모 조회 API를 완성합니다.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from typing import Any

from fastapi import FastAPI, HTTPException, Query


app = FastAPI(title="Memo Routing Lab Starter")


memos: dict[int, dict[str, Any]] = {
    1: {"id": 1, "title": "FastAPI 시작", "content": "라우팅을 연습합니다."},
    2: {"id": 2, "title": "Pydantic 준비", "content": "요청 검증을 배울 예정입니다."},
}


@app.get("/memos")
def list_memos():
    """TODO: 전체 메모 목록과 개수를 반환해 보세요."""

    return {"count": "TODO", "data": "TODO"}


@app.get("/memos/search")
def search_memos(
    keyword: str = Query(default="", description="검색어입니다."),
    limit: int = Query(default=10, ge=1, le=20, description="최대 결과 개수입니다."),
):
    """TODO: 제목 또는 본문에 keyword가 포함된 메모를 찾아보세요."""

    return {
        "keyword": keyword,
        "limit": limit,
        "data": "TODO",
    }


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int):
    """TODO: memo_id에 해당하는 메모 1개를 반환해 보세요."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return {"data": "TODO"}
