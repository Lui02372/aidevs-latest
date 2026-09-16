"""Gemini AI 답변을 Upstash Redis에 캐시합니다."""

from __future__ import annotations

import os
from urllib.parse import quote

import httpx
from fastapi import HTTPException, status

import app.core.config  # .env 파일을 읽습니다.
from app.core.gemini import get_gemini_client
from app.schemas.cache_schema import CachedAnswerResponse


TTL_SECONDS = 600


def redis_command(*parts: str) -> dict:
    """Upstash Redis REST API로 Redis 명령을 실행합니다.

    예: redis_command("get", "my-key")는 Redis의 GET my-key와 같은 의미입니다.
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

    # key나 value에 한글, 공백, 특수문자가 있어도 URL이 깨지지 않도록 인코딩합니다.
    encoded = [quote(part, safe="") for part in parts]
    url = f"{rest_url.rstrip('/')}/{'/'.join(encoded)}"
    headers = {"Authorization": f"Bearer {rest_token}"}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except httpx.HTTPError as error:
        raise HTTPException(status_code=502, detail=f"Redis 호출 실패: {error}") from error

    return response.json()


def cache_key(question: str) -> str:
    """질문 문자열을 Redis key로 변환합니다."""

    return f"ex90:answer:{question}"


def create_gemini_answer(question: str) -> str:
    """Gemini SDK로 답변을 만듭니다."""

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    client = get_gemini_client()
    try:
        response = client.models.generate_content(model=model, contents=question)
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Gemini 호출 실패: {error}") from error

    return response.text or ""


def get_or_create_answer(question: str) -> CachedAnswerResponse:
    """Redis에 답변이 있으면 재사용하고, 없으면 새 답변을 만들어 저장합니다."""

    key = cache_key(question)
    cached_result = redis_command("get", key)
    cached_answer = cached_result.get("result")

    if cached_answer:
        return CachedAnswerResponse(
            question=question,
            answer=cached_answer,
            cached=True,
            ttl_seconds=TTL_SECONDS,
        )

    answer = create_gemini_answer(question)
    # ex 옵션은 TTL(Time To Live)을 초 단위로 설정합니다.
    # 여기서는 60초 뒤 캐시가 자동 삭제됩니다.
    redis_command("set", key, answer, "ex", str(TTL_SECONDS))
    return CachedAnswerResponse(
        question=question,
        answer=answer,
        cached=False,
        ttl_seconds=TTL_SECONDS,
    )


def clear_answer(question: str) -> int:
    """특정 질문에 해당하는 Redis 캐시 key를 삭제합니다."""

    result = redis_command("del", cache_key(question))
    return int(result.get("result", 0))
