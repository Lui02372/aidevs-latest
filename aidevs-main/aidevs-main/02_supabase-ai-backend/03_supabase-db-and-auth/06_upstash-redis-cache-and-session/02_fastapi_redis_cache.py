r"""
FastAPI 응답을 Upstash Redis에 잠깐 저장하는 최소 예제입니다.

실행 위치:
    C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\06_upstash-redis-cache-and-session

실행 명령:
    ..\..\.venv\Scripts\Activate.ps1
    uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004

Swagger 확인:
    http://127.0.0.1:8004/docs

실행 전 준비:
    C:\aidevs\02_supabase-ai-backend\.env 파일에 아래 값이 있어야 합니다.

    UPSTASH_REDIS_REST_URL=https://...
    UPSTASH_REDIS_REST_TOKEN=...
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, status


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)

app = FastAPI(title="FastAPI Upstash Redis Cache Practice")


def redis_command(*parts: str) -> dict:
    """
    Upstash Redis REST API로 Redis 명령을 실행합니다.

    이 함수 하나로 get, set, ttl, del 같은 Redis 명령을 보냅니다.
    """

    rest_url = os.getenv("UPSTASH_REDIS_REST_URL")
    rest_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

    if not rest_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UPSTASH_REDIS_REST_URL이 없습니다. .env 파일을 확인하세요.",
        )

    if not rest_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UPSTASH_REDIS_REST_TOKEN이 없습니다. .env 파일을 확인하세요.",
        )

    rest_url = rest_url.rstrip("/")
    encoded_parts = [quote(part, safe="") for part in parts]
    command_url = f"{rest_url}/{'/'.join(encoded_parts)}"
    headers = {"Authorization": f"Bearer {rest_token}"}

    response = httpx.get(command_url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def create_mock_ai_answer(question: str) -> str:
    """
    실제 LLM 호출 대신 간단한 mock 답변을 만듭니다.

    이 예제의 목표는 LLM이 아니라 Redis 캐시 흐름입니다.
    그래서 비용이 드는 외부 AI API 호출은 하지 않습니다.
    """
    
    return f"'{question}'에 대한 임시 AI 답변입니다. Redis 캐시 흐름을 확인합니다."


@app.get("/health")
def health() -> dict[str, str | bool]:
    """FastAPI 서버와 Redis 환경변수 준비 상태를 확인합니다."""

    rest_url = os.getenv("UPSTASH_REDIS_REST_URL")
    rest_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

    return {
        "status": "ok",
        "redis": "upstash",
        "redis_url_configured": bool(rest_url),
        "redis_token_configured": bool(rest_token),
    }


@app.get("/ai/mock-answer")
def mock_answer(
    question: str = Query(min_length=1, examples=["Redis 캐시는 언제 쓰나요?"]),
) -> dict[str, str | bool | int]:
    """
    같은 질문이 들어오면 Redis에 저장해 둔 답변을 먼저 돌려줍니다.

    첫 번째 요청:
        Redis에 값이 없으므로 mock 답변을 새로 만들고 Redis에 저장합니다.

    두 번째 요청:
        같은 question이면 Redis에 저장된 답변을 바로 사용합니다.
    """

    ttl_seconds = 600
    cache_key = f"aidev:06:mock-answer:{question}"

    cached_result = redis_command("get", cache_key)
    cached_answer = cached_result.get("result")

    if cached_answer:
        return {
            "cached": True,
            "question": question,
            "answer": cached_answer,
            "ttl_seconds": ttl_seconds,
        }

    answer = create_mock_ai_answer(question)
    redis_command("set", cache_key, answer, "ex", str(ttl_seconds))

    return {
        "cached": False,
        "question": question,
        "answer": answer,
        "ttl_seconds": ttl_seconds,
    }


@app.delete("/ai/mock-answer-cache")
def clear_mock_answer_cache(
    question: str = Query(min_length=1, examples=["Redis 캐시는 언제 쓰나요?"]),
) -> dict[str, str | int]:
    """실습 중 같은 질문의 캐시를 지우고 싶을 때 사용합니다."""

    cache_key = f"aidev:06:mock-answer:{question}"
    deleted_result = redis_command("del", cache_key)

    return {
        "question": question,
        "cache_key": cache_key,
        "deleted_count": deleted_result.get("result", 0),
    }
