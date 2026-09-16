from app.core.config import SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL, is_supabase_configured
from app.services.memory_store import add_memory_log, recent_memory_logs


LAST_STORAGE_MODE = "memory"
LAST_STORAGE_ERROR = ""


def _mark_storage_status(mode: str, error: str = "") -> None:
    """최근 저장 모드와 오류 메시지를 health check에서 볼 수 있게 기록합니다."""

    global LAST_STORAGE_MODE, LAST_STORAGE_ERROR
    LAST_STORAGE_MODE = mode
    LAST_STORAGE_ERROR = error


def storage_status() -> dict[str, str | bool]:
    """현재 Supabase 설정 상태와 최근 저장 모드를 반환합니다."""

    configured = is_supabase_configured()
    expected_mode = "supabase" if configured else "memory"
    return {
        "supabase_configured": configured,
        "expected_storage_mode": expected_mode,
        "last_storage_mode": LAST_STORAGE_MODE,
        "last_storage_error": LAST_STORAGE_ERROR,
    }


def _client():
    """Supabase client를 준비합니다.

    Supabase 값이 없거나 `.env.example`의 예시 값이면 DB 대신 메모리 저장소를 사용합니다.
    이렇게 하면 수업 중 환경 설정이 늦어져도 API와 SSE 흐름을 먼저 확인할 수 있습니다.
    """

    if not is_supabase_configured():
        return None

    try:
        from supabase import create_client
    except ImportError:
        return None

    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def save_log(payload: dict) -> dict:
    """로그를 Supabase DB에 저장하고, DB를 쓸 수 없으면 메모리에 저장합니다."""

    client = _client()
    if client is None:
        item = add_memory_log(payload)
        item["storage_mode"] = "memory"
        _mark_storage_status("memory", "Supabase 환경변수가 없거나 supabase 패키지를 사용할 수 없습니다.")
        return item

    try:
        result = client.table("realtime_service_logs").insert(payload).execute()
    except Exception as exc:
        # schema.sql을 아직 실행하지 않았거나 Supabase 연결이 불안정하면
        # 실습이 멈추지 않도록 메모리 저장소로 fallback합니다.
        item = add_memory_log(payload)
        item["storage_mode"] = "memory"
        _mark_storage_status("memory", str(exc))
        return item

    if result.data:
        item = result.data[0]
        item["storage_mode"] = "supabase"
        _mark_storage_status("supabase")
        return item

    item = add_memory_log(payload)
    item["storage_mode"] = "memory"
    _mark_storage_status("memory", "Supabase insert 응답에 data가 없습니다.")
    return item


def list_logs(limit: int = 50) -> list[dict]:
    """최근 로그를 조회합니다. Supabase를 쓸 수 없으면 메모리 로그를 반환합니다."""

    client = _client()
    if client is None:
        _mark_storage_status("memory", "Supabase 환경변수가 없거나 supabase 패키지를 사용할 수 없습니다.")
        return recent_memory_logs(limit)

    try:
        result = (
            client.table("realtime_service_logs")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
    except Exception as exc:
        _mark_storage_status("memory", str(exc))
        return recent_memory_logs(limit)

    rows = result.data or []
    for row in rows:
        row["storage_mode"] = "supabase"
    _mark_storage_status("supabase")
    return rows


def summarize_logs() -> list[dict]:
    """최근 로그를 level별 개수로 집계합니다."""

    counts: dict[str, int] = {}
    for item in list_logs(200):
        level = item.get("level", "unknown")
        counts[level] = counts.get(level, 0) + 1
    return [{"level": level, "count": count} for level, count in sorted(counts.items())]
