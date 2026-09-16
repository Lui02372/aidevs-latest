r"""03_cached-ai-answer-api 라우트 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\03_cached-ai-answer-api
    python -m pytest tests

이 테스트는 Redis나 외부 LLM을 실제로 호출하지 않습니다.
FastAPI 앱이 정상적으로 import되는지, /health API가 응답하는지,
Gemini 답변 API와 Redis 캐시 API가 문서에 등록되어 있는지를 확인합니다.
초보자는 여기서 "기능 내부 구현을 다 검증하기 전에 API 경로부터 확인할 수 있다"는 흐름을 보면 됩니다.
"""

from fastapi.testclient import TestClient

from app.main import app


# TestClient는 FastAPI 앱을 메모리 안에서 실행해 요청과 응답을 확인합니다.
client = TestClient(app)


def test_health_route_is_ready() -> None:
    """기본 상태 확인 API가 200 OK와 status=ok를 반환하는지 확인합니다."""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_has_cache_routes() -> None:
    """Gemini 답변과 캐시 삭제 URL이 OpenAPI 문서에 있는지 확인합니다."""

    schema = client.get("/openapi.json").json()
    assert "/ai/answer" in schema["paths"]
    assert "/ai/answer-cache" in schema["paths"]
