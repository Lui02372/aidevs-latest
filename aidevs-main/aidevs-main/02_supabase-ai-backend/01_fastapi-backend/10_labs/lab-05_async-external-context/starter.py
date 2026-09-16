"""Lab 05 starter: 비동기 외부 API와 메모 컨텍스트 연결.

??:
    uvicorn starter:app --reload

? ???? ??? ??:
    python -m uvicorn starter:app --reload
"""

from typing import Any

import httpx
from fastapi import FastAPI, HTTPException


app = FastAPI(title="Async External Context Lab Starter")


memos: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "외부 API 연결",
        "content": "외부 데이터를 메모와 함께 응답합니다.",
        "tags": ["async", "external"],
    }
}


@app.get("/external/posts/{post_id}")
async def get_external_post(post_id: int):
    """TODO: 외부 API 원본 데이터와 가공 데이터를 함께 반환해 보세요."""

    external_data = await fetch_external_post(post_id)

    return {
        "source": "jsonplaceholder",
        "raw": external_data,
        "parsed": "TODO",
    }


@app.get("/memos/{memo_id}/external-context")
async def get_memo_with_external_context(memo_id: int, post_id: int = 1):
    """TODO: 메모와 외부 API 데이터를 하나의 응답으로 묶어 보세요."""

    if memo_id not in memos:
        raise HTTPException(status_code=404, detail="Memo not found")

    external_data = await fetch_external_post(post_id)

    return {
        "memo": "TODO",
        "external_context": "TODO",
    }


async def fetch_external_post(post_id: int) -> dict[str, Any]:
    """TODO: httpx.AsyncClient로 JSONPlaceholder API를 호출해 보세요."""

    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            response.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise HTTPException(status_code=error.response.status_code, detail="External API returned an error") from error
    except httpx.RequestError as error:
        raise HTTPException(status_code=503, detail="External API is not reachable") from error

    return response.json()
