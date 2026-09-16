from __future__ import annotations

import os
from datetime import datetime, timezone

import psycopg
from psycopg.types.json import Jsonb
from redis import Redis

from app.models import TaskRecord


QUEUE = "mini08:tasks"


def task_updated_at(task: TaskRecord):
    return task.updated_at


class RedisTasks:
    def __init__(self) -> None:
        self.client = Redis.from_url(
            os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
            decode_responses=True,
        )
        self.ttl = int(os.getenv("TASK_TTL_SECONDS", "3600"))

    def ping(self) -> bool:
        return bool(self.client.ping())

    def save(self, task: TaskRecord) -> TaskRecord:
        task.updated_at = datetime.now(timezone.utc)
        self.client.set(f"mini08:task:{task.task_id}", task.model_dump_json(), ex=self.ttl)
        return task

    def get(self, task_id: str) -> TaskRecord | None:
        raw = self.client.get(f"mini08:task:{task_id}")
        return TaskRecord.model_validate_json(raw) if raw else None

    def enqueue(self, task: TaskRecord) -> None:
        self.save(task)
        self.client.rpush(QUEUE, task.task_id)

    def dequeue(self, timeout: int = 5) -> str | None:
        item = self.client.blpop(QUEUE, timeout=timeout)
        return item[1] if item else None

    def find_idempotent(self, user_id: str, key: str) -> TaskRecord | None:
        task_id = self.client.get(f"mini08:idempotency:{user_id}:{key}")
        return self.get(task_id) if task_id else None

    def remember_idempotency(self, user_id: str, key: str, task_id: str) -> None:
        self.client.set(f"mini08:idempotency:{user_id}:{key}", task_id, ex=self.ttl)

    def active_tasks(self, limit: int = 20) -> list[TaskRecord]:
        tasks: list[TaskRecord] = []
        for key in self.client.scan_iter(match="mini08:task:*", count=100):
            raw = self.client.get(key)
            if raw:
                tasks.append(TaskRecord.model_validate_json(raw))
            if len(tasks) >= limit:
                break
        return sorted(tasks, key=task_updated_at, reverse=True)


class PostgresHistory:
    def __init__(self) -> None:
        self.url = os.getenv(
            "DATABASE_URL",
            "postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db",
        )

    def ping(self) -> bool:
        with psycopg.connect(self.url) as connection:
            return connection.execute("SELECT 1").fetchone()[0] == 1

    def save(self, task: TaskRecord) -> None:
        with psycopg.connect(self.url) as connection:
            connection.execute(
                """
                INSERT INTO mini_multi_agent_08.travel_task_runs
                    (task_id, trace_id, user_id, request, status, result, error)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (task_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    result = EXCLUDED.result,
                    error = EXCLUDED.error,
                    updated_at = NOW()
                """,
                (
                    task.task_id,
                    task.trace_id,
                    task.user_id,
                    task.request,
                    task.status,
                    Jsonb(task.result),
                    task.error,
                ),
            )
            for index, event in enumerate(task.trace, start=1):
                connection.execute(
                    """
                    INSERT INTO mini_multi_agent_08.travel_trace_events
                        (task_id, trace_id, sequence, actor, action, status, payload)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (task_id, sequence) DO NOTHING
                    """,
                    (
                        task.task_id,
                        task.trace_id,
                        index,
                        event.get("actor", "system"),
                        event.get("action", "unknown"),
                        event.get("status", "completed"),
                        Jsonb(event),
                    ),
                )

    def history(self, task_id: str, user_id: str) -> dict[str, object] | None:
        with psycopg.connect(self.url) as connection:
            task = connection.execute(
                """SELECT task_id, trace_id, status, result, error, created_at, updated_at
                   FROM mini_multi_agent_08.travel_task_runs WHERE task_id = %s AND user_id = %s""",
                (task_id, user_id),
            ).fetchone()
            if not task:
                return None
            events = connection.execute(
                """SELECT sequence, actor, action, status, payload, created_at
                   FROM mini_multi_agent_08.travel_trace_events WHERE task_id = %s ORDER BY sequence""",
                (task_id,),
            ).fetchall()
        return {
            "task": {
                "task_id": task[0], "trace_id": task[1], "status": task[2],
                "result": task[3], "error": task[4],
                "created_at": task[5].isoformat(), "updated_at": task[6].isoformat(),
            },
            "trace": [
                {"sequence": row[0], "actor": row[1], "action": row[2],
                 "status": row[3], "payload": row[4], "created_at": row[5].isoformat()}
                for row in events
            ],
        }

    def recent_runs(self, limit: int = 20) -> list[dict[str, object]]:
        with psycopg.connect(self.url) as connection:
            rows = connection.execute(
                """SELECT task_id, trace_id, user_id, status, error, created_at, updated_at
                   FROM mini_multi_agent_08.travel_task_runs
                   ORDER BY created_at DESC LIMIT %s""",
                (limit,),
            ).fetchall()
        return [
            {
                "task_id": row[0], "trace_id": row[1], "user_id": row[2],
                "status": row[3], "error": row[4],
                "created_at": row[5].isoformat(), "updated_at": row[6].isoformat(),
            }
            for row in rows
        ]

    def operation_summary(self) -> dict[str, object]:
        with psycopg.connect(self.url) as connection:
            status_rows = connection.execute(
                """SELECT status, COUNT(*)
                   FROM mini_multi_agent_08.travel_task_runs GROUP BY status"""
            ).fetchall()
            trace_rows = connection.execute(
                """SELECT actor, COUNT(*), COUNT(*) FILTER (WHERE status = 'failed')
                   FROM mini_multi_agent_08.travel_trace_events GROUP BY actor ORDER BY actor"""
            ).fetchall()
        return {
            "tasks_by_status": {row[0]: row[1] for row in status_rows},
            "agents": [
                {"actor": row[0], "events": row[1], "failures": row[2]}
                for row in trace_rows
            ],
        }
