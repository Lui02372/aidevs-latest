from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


TaskStatus = Literal["queued", "running", "waiting_approval", "completed", "rejected", "failed"]


def new_task_id() -> str:
    return f"task-{uuid4().hex[:12]}"


def new_trace_id() -> str:
    return f"trace-{uuid4().hex[:12]}"


def current_utc_time() -> datetime:
    return datetime.now(timezone.utc)


class TaskCreate(BaseModel):
    user_id: str = Field(min_length=3, max_length=100)
    request: str = Field(min_length=10, max_length=2000)
    idempotency_key: str = Field(min_length=5, max_length=200)


class TaskDecision(BaseModel):
    user_id: str
    decision: Literal["approve", "reject"]


class TaskRecord(BaseModel):
    task_id: str = Field(default_factory=new_task_id)
    trace_id: str = Field(default_factory=new_trace_id)
    user_id: str
    request: str
    status: TaskStatus = "queued"
    current_agent: str | None = None
    progress: int = Field(default=0, ge=0, le=100)
    result: dict[str, object] = Field(default_factory=dict)
    trace: list[dict[str, object]] = Field(default_factory=list)
    error: str | None = None
    created_at: datetime = Field(default_factory=current_utc_time)
    updated_at: datetime = Field(default_factory=current_utc_time)
