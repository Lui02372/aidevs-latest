r"""01_realtime-log-dashboard-practice backend 테스트 파일입니다.

실행:
    cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\backend
    C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
    python -m pytest tests -q

이 테스트는 실제 Supabase나 Upstash Redis가 없어도 통과하도록 구성되어 있습니다.
수업 초반에는 memory fallback으로 API가 정상 동작하는지 먼저 확인합니다.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.services.memory_store import logs


# TestClient는 uvicorn 서버를 직접 띄우지 않고도 FastAPI endpoint를 호출할 수 있게 해 줍니다.
client = TestClient(app)


def test_health() -> None:
    """GET /health가 backend 실행 상태를 정상적으로 반환하는지 확인합니다."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_list_logs() -> None:
    """POST /logs로 로그를 만들고, GET /logs로 다시 조회되는지 확인합니다."""

    # 이전 테스트에서 남은 memory log가 결과에 영향을 주지 않도록 비웁니다.
    logs.clear()

    payload = {
        "level": "info",
        "source": "test",
        "message": "테스트 로그입니다.",
        "request_path": "/test",
        "status_code": 200,
        "latency_ms": 10,
        "metadata": {"test": True},
    }

    create_response = client.post("/logs", json=payload)
    assert create_response.status_code == 200
    assert create_response.json()["message"] == "테스트 로그입니다."

    list_response = client.get("/logs")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1


def test_log_summary() -> None:
    """GET /logs/summary가 level별 로그 개수 목록을 반환하는지 확인합니다."""

    response = client.get("/logs/summary")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
