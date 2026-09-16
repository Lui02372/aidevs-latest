from fastapi import FastAPI, HTTPException

from app.models import TaskCreate, TaskDecision, TaskRecord
from app.repositories import PostgresHistory, RedisTasks
from app.observability import structured_log


app = FastAPI(title="Travel Multi AI Agent Service", version="1.0.0")


def redis_tasks() -> RedisTasks:
    return RedisTasks()


def postgres_history() -> PostgresHistory:
    return PostgresHistory()


def require_user_task(task_id: str, user_id: str) -> TaskRecord:
    task = redis_tasks().get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task를 찾을 수 없습니다.")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="다른 사용자의 Task입니다.")
    return task


@app.get("/health")
def health() -> dict[str, object]:
    checks: dict[str, object] = {}
    for name, repository in (("redis", redis_tasks()), ("postgresql", postgres_history())):
        try:
            checks[name] = repository.ping()
        except Exception as error:
            checks[name] = f"{type(error).__name__}: {error}"
    return {"status": "ok" if checks == {"redis": True, "postgresql": True} else "degraded", **checks}


@app.get("/health/live")
def liveness() -> dict[str, str]:
    """Process가 HTTP 요청에 응답할 수 있는지만 확인합니다."""
    return {"status": "alive"}


@app.get("/health/ready")
def readiness() -> dict[str, object]:
    """Redis와 PostgreSQL을 포함해 Task 처리 준비 여부를 확인합니다."""
    checks = health()
    if checks["status"] != "ok":
        raise HTTPException(status_code=503, detail=checks)
    return {"status": "ready", "dependencies": checks}


@app.post("/api/tasks", response_model=TaskRecord, status_code=202)
def create_task(payload: TaskCreate) -> TaskRecord:
    repository = redis_tasks()
    existing = repository.find_idempotent(payload.user_id, payload.idempotency_key)
    if existing:
        return existing
    task = TaskRecord(user_id=payload.user_id, request=payload.request)
    task.trace.append({"actor": payload.user_id, "action": "enqueue", "status": "completed"})
    repository.enqueue(task)
    repository.remember_idempotency(payload.user_id, payload.idempotency_key, task.task_id)
    postgres_history().save(task)
    structured_log("info", "task_queued", task_id=task.task_id, trace_id=task.trace_id, actor=payload.user_id)
    return task


@app.get("/api/tasks/{task_id}", response_model=TaskRecord)
def get_task(task_id: str, user_id: str) -> TaskRecord:
    return require_user_task(task_id, user_id)


@app.get("/api/tasks/{task_id}/history")
def get_history(task_id: str, user_id: str) -> dict[str, object]:
    require_user_task(task_id, user_id)
    history = postgres_history().history(task_id, user_id)
    if history is None:
        raise HTTPException(status_code=404, detail="영구 이력을 찾을 수 없습니다.")
    return history


@app.post("/api/tasks/{task_id}/decision", response_model=TaskRecord)
def decide(task_id: str, payload: TaskDecision) -> TaskRecord:
    task = require_user_task(task_id, payload.user_id)
    if task.status != "waiting_approval":
        raise HTTPException(status_code=409, detail="승인 대기 Task가 아닙니다.")
    if payload.decision == "approve":
        task.status = "completed"
        task.progress = 100
        task.trace.append({"actor": payload.user_id, "action": "approve", "status": "completed"})
    else:
        task.status = "rejected"
        task.trace.append({"actor": payload.user_id, "action": "reject", "status": "completed"})
    redis_tasks().save(task)
    postgres_history().save(task)
    structured_log("info", f"task_{task.status}", task_id=task.task_id, trace_id=task.trace_id, actor=payload.user_id)
    return task


@app.get("/api/operations/live")
def live_tasks() -> list[dict[str, object]]:
    return [task.model_dump(mode="json") for task in redis_tasks().active_tasks()]


@app.get("/api/operations/history")
def recent_history() -> list[dict[str, object]]:
    return postgres_history().recent_runs()


@app.get("/api/operations/summary")
def operations_summary() -> dict[str, object]:
    live = redis_tasks().active_tasks()
    return {"live_task_count": len(live), **postgres_history().operation_summary()}
