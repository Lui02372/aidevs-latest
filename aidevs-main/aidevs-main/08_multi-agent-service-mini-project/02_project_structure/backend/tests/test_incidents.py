"""backend API 기본 테스트입니다.

실행 방법:
    cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
    pytest backend\tests
"""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_incident() -> None:
    response = client.post(
        "/incidents",
        json={
            "service_name": "backend",
            "message": "backend timeout occurred",
            "severity": "medium",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["failure_type"] == "network_timeout"
    assert body["selected_strategy"] == "retry_with_backoff"
