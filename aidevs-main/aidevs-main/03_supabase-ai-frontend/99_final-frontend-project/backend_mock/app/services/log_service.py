from datetime import datetime, timezone
from uuid import uuid4

from app.services.memory_store import service_logs


def now_text() -> str:
    """로그 저장에 사용할 현재 UTC 시간을 ISO 문자열로 반환합니다."""

    return datetime.now(timezone.utc).isoformat()


def add_log(
    action: str,
    status: str,
    detail: str | None = None,
    user_email: str | None = None,
) -> dict:
    """서비스 이벤트 하나를 메모리 로그 목록에 추가합니다."""

    item = {
        "id": str(uuid4()),
        "user_email": user_email,
        "action": action,
        "status": status,
        "detail": detail,
        "created_at": now_text(),
    }
    service_logs.append(item)
    return item


def list_logs_for_user(user_email: str) -> list[dict]:
    """공통 로그와 현재 사용자 로그를 최신순으로 반환합니다."""

    return [
        item
        for item in reversed(service_logs)
        if item["user_email"] in (None, user_email)
    ]
