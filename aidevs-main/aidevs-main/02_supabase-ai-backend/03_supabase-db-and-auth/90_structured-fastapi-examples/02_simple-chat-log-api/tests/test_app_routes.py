r"""02_simple-chat-log-api 라우트 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\02_simple-chat-log-api
    python -m pytest tests

이 테스트는 채팅 로그를 실제 Supabase에 저장하는 통합 테스트가 아닙니다.
FastAPI 앱이 정상적으로 준비되는지, /health API가 응답하는지,
Swagger/OpenAPI 문서에 /chat, /logs URL이 등록되어 있는지를 확인합니다.
처음에는 이런 "라우트 존재 확인 테스트"만으로도 프로젝트 구조가 깨졌는지 빠르게 알 수 있습니다.
"""

from fastapi.testclient import TestClient

from app.main import app


# TestClient는 브라우저나 Postman 대신 테스트 코드에서 API를 호출하는 도구입니다.
client = TestClient(app)


def test_health_route_is_ready() -> None:
    """서버 상태 확인용 /health API가 정상 동작하는지 확인합니다."""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_has_chat_routes() -> None:
    """채팅 요청과 로그 조회 API가 OpenAPI 문서에 포함되어 있는지 확인합니다."""

    schema = client.get("/openapi.json").json()
    assert "/chat" in schema["paths"]
    assert "/logs" in schema["paths"]
