r"""01_notes-api-with-supabase 라우트 테스트입니다.

실행 방법:
    cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\01_notes-api-with-supabase
    python -m pytest tests

이 테스트는 실제 Supabase에 데이터를 넣고 조회하는 테스트가 아닙니다.
FastAPI 앱이 정상적으로 import되는지, /health API가 응답하는지,
Swagger/OpenAPI 문서에 notes 관련 URL이 등록되어 있는지를 확인합니다.
초보자는 이 파일을 통해 "API 서버를 직접 실행하지 않아도 TestClient로 API를 호출할 수 있다"는 점을 이해하면 됩니다.
"""

from fastapi.testclient import TestClient

from app.main import app


# TestClient는 FastAPI 앱을 테스트 코드 안에서 직접 호출할 수 있게 해 줍니다.
# uvicorn 서버를 따로 켜지 않아도 GET/POST 요청을 흉내 낼 수 있습니다.
client = TestClient(app)


def test_health_route_is_ready() -> None:
    """기본 상태 확인 API인 /health가 정상 응답하는지 확인합니다."""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_has_notes_routes() -> None:
    """OpenAPI 문서에 notes 생성/조회용 URL이 등록되어 있는지 확인합니다."""

    schema = client.get("/openapi.json").json()
    assert "/notes" in schema["paths"]
    assert "/notes/{note_id}" in schema["paths"]
