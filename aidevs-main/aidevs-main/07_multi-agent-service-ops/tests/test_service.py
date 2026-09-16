import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
SERVICE_ROOT = ROOT / "08_multi-ai-agent-service"
sys.path.insert(0, str(SERVICE_ROOT))

from app.models import TaskRecord  # noqa: E402
from app import service  # noqa: E402
import backend  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from shared.travel_contracts import RouteDecision, SpecialistResult  # noqa: E402


def result(agent_id: str) -> SpecialistResult:
    return SpecialistResult(
        agent_id=agent_id,
        goal="여행 전문 작업",
        summary=f"{agent_id} 결과",
        recommendations=["추천"],
        completed=True,
    )


def test_service_orchestrates_specialists_and_waits_for_approval(monkeypatch) -> None:
    monkeypatch.setattr(
        service,
        "route",
        lambda task: RouteDecision(
            selected_agents=["weather_agent", "place_agent", "budget_agent"],
            reason="필수 조건 확인",
        ),
    )
    monkeypatch.setattr(service, "specialist", lambda task, agent_id: result(agent_id))
    monkeypatch.setattr(service, "itinerary", lambda task, results: result("itinerary_agent"))
    task = TaskRecord(user_id="user-1", request="부산 2박 3일 여행을 계획해 주세요.")

    completed = service.run_multi_agent(task)

    assert completed.status == "waiting_approval"
    assert completed.progress == 90
    assert set(completed.result["specialists"]) == {
        "weather_agent",
        "place_agent",
        "budget_agent",
    }
    assert completed.result["itinerary"]["agent_id"] == "itinerary_agent"
    assert completed.trace[-1]["action"] == "wait_for_approval"


class FakeRedisClient:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.queue: list[str] = []

    def set(self, key, value, ex=None):
        self.values[key] = value

    def get(self, key):
        return self.values.get(key)

    def rpush(self, key, value):
        self.queue.append(value)

    def blpop(self, key, timeout=0):
        return (key, self.queue.pop(0)) if self.queue else None

    def ping(self):
        return True


def test_redis_repository_keeps_task_queue_and_user_idempotency() -> None:
    from app.repositories import RedisTasks

    repository = RedisTasks.__new__(RedisTasks)
    repository.client = FakeRedisClient()
    repository.ttl = 60
    task = TaskRecord(user_id="user-1", request="부산 여행 계획을 만들어 주세요.")
    repository.enqueue(task)
    repository.remember_idempotency("user-1", "request-1", task.task_id)

    assert repository.dequeue(timeout=0) == task.task_id
    assert repository.get(task.task_id).user_id == "user-1"
    assert repository.find_idempotent("user-1", "request-1").task_id == task.task_id
    assert repository.find_idempotent("user-2", "request-1") is None


class MemoryTasks:
    def __init__(self) -> None:
        self.tasks = {}
        self.keys = {}

    def get(self, task_id):
        return self.tasks.get(task_id)

    def save(self, task):
        self.tasks[task.task_id] = task
        return task

    def enqueue(self, task):
        self.save(task)

    def find_idempotent(self, user_id, key):
        task_id = self.keys.get((user_id, key))
        return self.get(task_id) if task_id else None

    def remember_idempotency(self, user_id, key, task_id):
        self.keys[(user_id, key)] = task_id


class MemoryHistory:
    def __init__(self) -> None:
        self.saved = []

    def save(self, task):
        self.saved.append(task.model_copy(deep=True))


def test_backend_scopes_idempotency_and_approval_to_user(monkeypatch) -> None:
    tasks = MemoryTasks()
    history = MemoryHistory()
    monkeypatch.setattr(backend, "redis_tasks", lambda: tasks)
    monkeypatch.setattr(backend, "postgres_history", lambda: history)
    client = TestClient(backend.app)
    payload = {
        "user_id": "user-1",
        "request": "부산으로 2박 3일 여행 계획을 만들어 주세요.",
        "idempotency_key": "same-request",
    }

    first = client.post("/api/tasks", json=payload)
    repeated = client.post("/api/tasks", json=payload)
    assert first.status_code == 202
    assert repeated.json()["task_id"] == first.json()["task_id"]

    task = tasks.get(first.json()["task_id"])
    task.status = "waiting_approval"
    tasks.save(task)
    forbidden = client.post(
        f"/api/tasks/{task.task_id}/decision",
        json={"user_id": "user-2", "decision": "approve"},
    )
    approved = client.post(
        f"/api/tasks/{task.task_id}/decision",
        json={"user_id": "user-1", "decision": "approve"},
    )
    assert forbidden.status_code == 403
    assert approved.status_code == 200
    assert approved.json()["status"] == "completed"
