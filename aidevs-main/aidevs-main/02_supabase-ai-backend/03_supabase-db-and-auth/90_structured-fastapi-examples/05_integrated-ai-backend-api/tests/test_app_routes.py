r"""05_integrated-ai-backend-api 라우트 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\05_integrated-ai-backend-api
    python -m pytest tests

이 테스트는 통합 예제의 모든 기능을 실제로 끝까지 호출하지 않습니다.
FastAPI 앱이 정상적으로 import되는지, /health API가 응답하는지,
인증, 사용자 정보, 채팅, 로그 관련 핵심 URL이 OpenAPI 문서에 등록되어 있는지를 확인합니다.
통합 프로젝트에서는 파일 구조가 많아지기 때문에, 이런 라우트 테스트가 깨지면 main.py 또는 router 연결부터 확인하면 됩니다.
"""

from fastapi.testclient import TestClient

from app.main import app


# TestClient는 서버를 따로 실행하지 않고 FastAPI 앱에 요청을 보내는 테스트용 클라이언트입니다.
client = TestClient(app)


def test_health_route_is_ready() -> None:
    """통합 예제 앱의 /health API가 정상 응답하는지 확인합니다."""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_has_integrated_routes() -> None:
    """통합 예제에 필요한 핵심 API 경로가 모두 등록되어 있는지 확인합니다."""

    schema = client.get("/openapi.json").json()
    assert "/auth/signup" in schema["paths"]
    assert "/auth/signin" in schema["paths"]
    assert "/me" in schema["paths"]
    assert "/chat" in schema["paths"]
    assert "/logs" in schema["paths"]
    assert "HTTPBearer" in schema["components"]["securitySchemes"]
