"""Redis 멀티턴 채팅 API의 기본 라우트를 확인합니다."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_route_is_ready() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_has_multi_turn_redis_routes() -> None:
    schema = client.get("/openapi.json").json()

    assert "/chat" in schema["paths"]
    assert "/conversations/{conversation_id}/messages" in schema["paths"]
    assert "/conversations/{conversation_id}" in schema["paths"]
