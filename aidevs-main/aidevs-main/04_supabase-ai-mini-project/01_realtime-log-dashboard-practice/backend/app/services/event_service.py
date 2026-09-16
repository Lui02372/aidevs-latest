import asyncio
import json
from datetime import datetime, timezone

from app.core.config import REDIS_CHANNEL, REDIS_URL, is_redis_configured
from app.services.memory_store import (
    publish_memory_event,
    subscribe_memory,
    unsubscribe_memory,
)


LAST_EVENT_MODE = "memory"
LAST_EVENT_ERROR = ""
HEARTBEAT_SECONDS = 10


def heartbeat_event() -> dict:
    """SSE 연결이 끊기지 않도록 주기적으로 보내는 heartbeat 이벤트입니다."""

    return {
        "_sse_event": "heartbeat",
        "message": "SSE 연결 유지 중입니다.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def _mark_event_status(mode: str, error: str = "") -> None:
    """최근 이벤트 전달 모드와 오류 메시지를 health check에서 볼 수 있게 기록합니다."""

    global LAST_EVENT_MODE, LAST_EVENT_ERROR
    LAST_EVENT_MODE = mode
    LAST_EVENT_ERROR = error


def event_status() -> dict[str, str | bool]:
    """현재 Redis 설정 상태와 최근 이벤트 전달 모드를 반환합니다."""

    configured = is_redis_configured()
    expected_mode = "upstash-redis" if configured else "memory"
    return {
        "redis_configured": configured,
        "expected_event_mode": expected_mode,
        "last_event_mode": LAST_EVENT_MODE,
        "last_event_error": LAST_EVENT_ERROR,
    }


async def publish_log_event(item: dict) -> None:
    """새 로그 이벤트를 Upstash Redis 또는 메모리 큐로 전달합니다.

    REDIS_URL이 있으면 Upstash Redis pub/sub을 사용하고,
    없거나 연결에 실패하면 수업용 memory queue로 fallback합니다.
    """

    if is_redis_configured():
        try:
            import redis.asyncio as redis

            client = redis.from_url(REDIS_URL, decode_responses=True)
            await client.publish(REDIS_CHANNEL, json.dumps(item, ensure_ascii=False))
            await client.aclose()
            _mark_event_status("upstash-redis")
            return
        except Exception as exc:
            _mark_event_status("memory", str(exc))

    await publish_memory_event(item)
    if not is_redis_configured():
        _mark_event_status("memory", "REDIS_URL이 없어 memory queue를 사용합니다.")


async def redis_event_stream():
    """Upstash Redis pub/sub 채널에서 새 로그 이벤트를 계속 읽습니다."""

    import redis.asyncio as redis

    client = redis.from_url(REDIS_URL, decode_responses=True)
    pubsub = client.pubsub()
    await pubsub.subscribe(REDIS_CHANNEL)
    last_heartbeat = asyncio.get_running_loop().time()

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message.get("data"):
                _mark_event_status("upstash-redis")
                yield json.loads(message["data"])

            now = asyncio.get_running_loop().time()
            if now - last_heartbeat >= HEARTBEAT_SECONDS:
                yield heartbeat_event()
                last_heartbeat = now

            await asyncio.sleep(0.1)
    finally:
        await pubsub.unsubscribe(REDIS_CHANNEL)
        await pubsub.aclose()
        await client.aclose()


async def memory_event_stream():
    """Upstash Redis URL이 없을 때 사용할 메모리 기반 SSE 이벤트 스트림입니다."""

    queue = subscribe_memory()
    try:
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=HEARTBEAT_SECONDS)
                yield item
            except asyncio.TimeoutError:
                yield heartbeat_event()
    finally:
        unsubscribe_memory(queue)


async def event_stream():
    """SSE endpoint가 사용할 이벤트 스트림을 선택합니다."""

    if is_redis_configured():
        try:
            async for item in redis_event_stream():
                yield item
            return
        except Exception as exc:
            _mark_event_status("memory", str(exc))

    async for item in memory_event_stream():
        yield item
