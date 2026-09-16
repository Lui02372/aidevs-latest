"""멀티턴 채팅 API의 기본 라우트를 확인합니다."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_route_is_ready() -> None:
    """환경변수가 없어도 상태 확인 API는 호출할 수 있습니다."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_has_multi_turn_routes() -> None:
    """채팅과 대화 이력 조회 API가 문서에 등록되었는지 확인합니다."""

    schema = client.get("/openapi.json").json()

    assert "/chat" in schema["paths"]
    assert "/conversations/{conversation_id}/messages" in schema["paths"]
