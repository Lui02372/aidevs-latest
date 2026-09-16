r"""04_auth-jwt-profile-api 라우트 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\04_auth-jwt-profile-api
    python -m pytest tests

이 테스트는 실제 회원가입, 로그인, JWT 검증을 수행하지 않습니다.
대신 FastAPI 앱이 정상적으로 준비되는지, /health API가 응답하는지,
Auth와 Profile 관련 URL이 Swagger/OpenAPI 문서에 등록되어 있는지를 확인합니다.
인증 API는 외부 서비스와 연결될 수 있으므로, 처음에는 라우트 존재 여부부터 확인하는 방식이 안전합니다.
"""

from fastapi.testclient import TestClient

from app.main import app


# TestClient는 테스트 중에 FastAPI 앱을 직접 호출하는 간단한 클라이언트입니다.
client = TestClient(app)


def test_health_route_is_ready() -> None:
    """인증 예제 앱의 /health API가 정상 응답하는지 확인합니다."""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_has_auth_and_profile_routes() -> None:
    """회원가입, 로그인, 내 정보, 프로필 API 경로가 등록되어 있는지 확인합니다."""

    schema = client.get("/openapi.json").json()
    assert "/auth/signup" in schema["paths"]
    assert "/auth/signin" in schema["paths"]
    assert "/me" in schema["paths"]
    assert "/profile" in schema["paths"]
