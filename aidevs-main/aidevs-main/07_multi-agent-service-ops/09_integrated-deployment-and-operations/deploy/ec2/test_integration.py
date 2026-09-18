"""Real PostgreSQL + Redis + API check. Runs only against disposable CI services."""
import os
import sys
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "08_multi-ai-agent-service"))


@pytest.mark.skipif(os.getenv("RUN_DEPLOY_INTEGRATION") != "1", reason="Requires disposable CI DB and Redis")
def test_api_persists_task_and_trace():
    from fastapi.testclient import TestClient
    from backend import app
    from app.repositories import RedisTasks

    task_id = None
    key = uuid4().hex
    tasks = RedisTasks()
    try:
        with TestClient(app) as client:
            assert client.get("/health/ready").status_code == 200
            response = client.post("/api/tasks", json={
                "user_id": "ci-user", "request": "서울 여행 계획을 만들어 주세요", "idempotency_key": key,
            })
            assert response.status_code == 202, response.text
            task_id = response.json()["task_id"]
            history = client.get(f"/api/tasks/{task_id}/history", params={"user_id": "ci-user"})
            assert history.status_code == 200
            assert history.json()["task"]["status"] == "queued"
            assert history.json()["trace"][0]["action"] == "enqueue"
            with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
                assert conn.execute("SELECT user_id FROM mini_multi_agent_08.travel_task_runs WHERE task_id=%s", (task_id,)).fetchone() == ("ci-user",)
    finally:
        if task_id:
            with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
                conn.execute("DELETE FROM mini_multi_agent_08.travel_task_runs WHERE task_id=%s", (task_id,))
            tasks.client.lrem("mini08:tasks", 0, task_id)
            tasks.client.delete(f"mini08:task:{task_id}", f"mini08:idempotency:ci-user:{key}")
