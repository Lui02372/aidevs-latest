from fastapi.testclient import TestClient

from app.main import app


# TestClient는 실제 uvicorn 서버를 띄우지 않고 FastAPI app을 직접 호출합니다.
client = TestClient(app)


def test_health() -> None:
    """환경변수 없이도 /health endpoint는 정상 응답해야 합니다."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_protected_api_requires_token() -> None:
    """보호된 API는 Authorization header가 없으면 401을 반환해야 합니다."""

    response = client.get("/me")

    assert response.status_code == 401
