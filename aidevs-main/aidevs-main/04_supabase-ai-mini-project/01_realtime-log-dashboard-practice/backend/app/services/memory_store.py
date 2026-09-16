"""Supabase 또는 Upstash Redis 없이도 실습을 이어가기 위한 memory 저장소입니다.

이 파일은 서버가 실행 중인 동안만 데이터를 기억합니다.
서버를 끄고 다시 실행하면 `logs`와 `subscribers`는 모두 초기화됩니다.

수업에서 이 파일을 두는 이유:
    1. Supabase 테이블을 아직 만들지 않았어도 로그 API를 먼저 테스트할 수 있습니다.
    2. Upstash Redis URL이 없어도 SSE 실시간 화면 흐름을 먼저 확인할 수 있습니다.
    3. 이후 Supabase/Upstash Redis를 연결했을 때 무엇이 달라지는지 비교할 수 있습니다.
"""

from datetime import datetime, timezone
from uuid import uuid4
import asyncio


# logs:
#   Supabase를 사용하지 못할 때 임시로 로그를 저장하는 리스트입니다.
# subscribers:
#   SSE로 실시간 로그를 기다리는 브라우저 연결들을 큐 형태로 저장합니다.
logs: list[dict] = []
subscribers: list[asyncio.Queue] = []


def now_text() -> str:
    """현재 시간을 ISO 문자열로 만듭니다."""

    return datetime.now(timezone.utc).isoformat()


def add_memory_log(payload: dict) -> dict:
    """새 로그에 id와 created_at을 붙여 메모리에 저장합니다."""

    item = {
        "id": str(uuid4()),
        "created_at": now_text(),
        **payload,
    }
    logs.insert(0, item)
    return item


def recent_memory_logs(limit: int = 50) -> list[dict]:
    """가장 최근 로그부터 limit 개수만큼 반환합니다."""

    return logs[:limit]


async def publish_memory_event(item: dict) -> None:
    """SSE를 기다리는 모든 브라우저 연결에 새 로그를 전달합니다."""

    for queue in list(subscribers):
        await queue.put(item)


def subscribe_memory() -> asyncio.Queue:
    """새 SSE 연결이 생겼을 때 해당 연결 전용 queue를 등록합니다."""

    queue: asyncio.Queue = asyncio.Queue()
    subscribers.append(queue)
    return queue


def unsubscribe_memory(queue: asyncio.Queue) -> None:
    """브라우저 연결이 끊어졌을 때 queue를 목록에서 제거합니다."""

    if queue in subscribers:
        subscribers.remove(queue)
