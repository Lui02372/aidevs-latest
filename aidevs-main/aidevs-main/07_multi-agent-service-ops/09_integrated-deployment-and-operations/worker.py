"""
[통합 Worker 시나리오]
API가 Redis Queue에 넣은 여행 Task를 Worker가 가져옵니다. Worker는 실제 AI Agent와
HTTP MCP 날씨 Tool을 사용해 협업을 실행하고, Redis에 현재 상태를, PostgreSQL에 실행
이력을 저장합니다. Docker에서는 API와 Worker를 서로 다른 Process로 분리합니다.
"""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path


COURSE_ROOT = Path(__file__).resolve().parents[1]
SERVICE_ROOT = COURSE_ROOT / "08_multi-ai-agent-service"
sys.path.insert(0, str(SERVICE_ROOT))

from app.repositories import PostgresHistory, RedisTasks  # noqa: E402
from integrated_orchestrator import run_integrated  # noqa: E402


def process_one(tasks: RedisTasks, history: PostgresHistory, timeout: int = 5):
    task_id = tasks.dequeue(timeout=timeout)
    if task_id is None:
        return None
    task = tasks.get(task_id)
    if task is None or task.status != "queued":
        return None
    try:
        task = asyncio.run(run_integrated(task))
    except Exception as error:
        task.status = "failed"
        task.error = f"{type(error).__name__}: {error}"
        task.trace.append(
            {
                "actor": "integrated_worker",
                "action": "orchestrate",
                "status": "failed",
                "error_type": type(error).__name__,
                "error": str(error),
            }
        )
    tasks.save(task)
    history.save(task)
    return task


def main() -> None:
    tasks = RedisTasks()
    history = PostgresHistory()
    tasks.ping()
    history.ping()
    print("Integrated Worker가 Redis Queue를 기다립니다. 종료: Ctrl+C")
    while True:
        task = process_one(tasks, history)
        if task:
            print(task.task_id, task.status)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Worker를 종료합니다.")
    except Exception:
        time.sleep(1)
        raise
