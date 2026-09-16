from __future__ import annotations

import json
import logging
from datetime import datetime, timezone


LOGGER = logging.getLogger("multi_agent_service")
if not LOGGER.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


def structured_log(
    level: str,
    event: str,
    *,
    task_id: str | None = None,
    trace_id: str | None = None,
    actor: str = "system",
    details: dict[str, object] | None = None,
) -> dict[str, object]:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "event": event,
        "task_id": task_id,
        "trace_id": trace_id,
        "actor": actor,
        "details": details or {},
    }
    getattr(LOGGER, level.lower(), LOGGER.info)(json.dumps(record, ensure_ascii=False))
    return record
