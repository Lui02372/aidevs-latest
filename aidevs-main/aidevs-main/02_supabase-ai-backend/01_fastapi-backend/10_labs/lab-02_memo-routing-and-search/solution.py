"""Lab 02 solution: 메모 라우팅과 검색.

??:
    uvicorn solution:app --reload

? ???? ??? ??:
    python -m uvicorn solution:app --reload
"""

from typing import Any

from fastapi import FastAPI, HTTPException, Query


app = FastAPI(title="Memo Routing Lab")


memos: dict[int, dict[str, Any]] = {
    1: {"id": 1, "title": "FastAPI 시작", "content": "라우팅을 연습합니다."},
    2: {"id": 2, "title": "Pydantic 준비", "content": "요청 검증을 배울 예정입니다."},
    3: {"id": 3, "title": "외부 API", "content": "비동기 호출 구조를 이해합니다."},
}


@app.get("/memos")
def list_memos():
    """전체 메모 목록과 개수를 반환합니다."""

    memo_list = list(memos.values())
    return {"count": len(memo_list), "data": memo_list}


@app.get("/memos/search")
def search_memos(
    keyword: str = Query(default="", description="검색어입니다."),
    limit: int = Query(default=10, ge=1, le=20, description="최대 결과 개수입니다."),
):
    """제목 또는 본문에 검색어가 포함된 메모를 반환합니다."""

    normalized_keyword = keyword.lower()
    result = [
        memo
        for memo in memos.values()
        if normalized_keyword in memo["title"].lower()
        or normalized_keyword in memo["content"].lower()
    ]

    return {
        "keyword": keyword,
        "limit": limit,
        "count": len(result[:limit]),
        "data": result[:limit],
    }


@app.get("/memos/{memo_id}")
def get_memo(memo_id: int):
    """memo_id에 해당하는 메모 1개를 반환합니다."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    return {"data": memos[memo_id]}
