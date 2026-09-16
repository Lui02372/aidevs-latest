import hashlib
import json
from urllib.parse import quote

import httpx

from app.core.config import UPSTASH_REDIS_REST_TOKEN, UPSTASH_REDIS_REST_URL


def _cache_enabled() -> bool:
    """Upstash Redis 환경변수가 모두 있을 때만 캐시 기능을 켭니다."""

    return bool(UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN)


def make_cache_key(user_id: str, message: str) -> str:
    """사용자와 질문 내용을 이용해 Redis key를 만듭니다.

    질문 원문 전체를 key에 그대로 쓰지 않고 hash로 바꾸면 길이와 특수문자 문제를 줄일 수 있습니다.
    """

    digest = hashlib.sha256(message.strip().lower().encode("utf-8")).hexdigest()
    return f"frontend-chat:{user_id}:{digest}"


def get_cached_answer(cache_key: str) -> str | None:
    """Redis에서 이전에 저장된 답변을 조회합니다."""

    if not _cache_enabled():
        return None

    # Upstash REST API는 URL 경로에 key가 들어가므로 안전하게 URL 인코딩합니다.
    encoded_key = quote(cache_key, safe="")
    url = f"{UPSTASH_REDIS_REST_URL.rstrip('/')}/get/{encoded_key}"
    headers = {"Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}"}
    response = httpx.get(url, headers=headers, timeout=5.0)
    response.raise_for_status()

    value = response.json().get("result")
    if not value:
        return None

    return json.loads(value)["answer"]


def set_cached_answer(cache_key: str, answer: str) -> None:
    """Redis에 AI 답변을 저장합니다."""

    if not _cache_enabled():
        return

    # 한글 답변이 깨지지 않도록 ensure_ascii=False로 JSON 문자열을 만듭니다.
    payload = json.dumps({"answer": answer}, ensure_ascii=False)
    encoded_key = quote(cache_key, safe="")
    encoded_payload = quote(payload, safe="")
    url = f"{UPSTASH_REDIS_REST_URL.rstrip('/')}/set/{encoded_key}/{encoded_payload}"
    headers = {"Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}"}
    response = httpx.post(url, headers=headers, timeout=5.0)
    response.raise_for_status()
