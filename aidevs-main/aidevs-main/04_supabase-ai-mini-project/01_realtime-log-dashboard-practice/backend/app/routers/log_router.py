import json
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.log_schema import LogCreate, LogItem, LogSummary
from app.services.db_service import list_logs, save_log, summarize_logs
from app.services.event_service import event_stream, publish_log_event


router = APIRouter(tags=["logs"])


@router.post("/logs", response_model=LogItem)
async def create_log(payload: LogCreate) -> dict:
    """로그를 저장하고 실시간 이벤트로 발행합니다."""

    item = save_log(payload.model_dump())
    await publish_log_event(item)
    return item


@router.get("/logs", response_model=list[LogItem])
def get_logs(limit: int = 50) -> list[dict]:
    """최근 로그 목록을 반환합니다."""

    return list_logs(limit)


@router.get("/logs/summary", response_model=list[LogSummary])
def get_log_summary() -> list[dict]:
    """level별 로그 개수를 반환합니다."""

    return summarize_logs()


@router.get("/stream/logs")
async def stream_logs() -> StreamingResponse:
    """SSE 형식으로 새 로그 이벤트를 브라우저에 계속 전달합니다."""

    async def generate():
        connected = {
            "message": "SSE 연결이 열렸습니다. 새 로그가 생성되면 event: log로 전달됩니다.",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        yield f"event: connected\ndata: {json.dumps(connected, ensure_ascii=False)}\n\n"

        async for item in event_stream():
            payload = dict(item)
            event_name = payload.pop("_sse_event", "log")
            data = json.dumps(payload, ensure_ascii=False)
            yield f"event: {event_name}\ndata: {data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
