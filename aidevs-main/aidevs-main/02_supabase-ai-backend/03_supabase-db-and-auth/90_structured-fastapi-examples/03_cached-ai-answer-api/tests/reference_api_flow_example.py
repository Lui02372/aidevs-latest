# 바이브 코딩 프롬프트 예시:
# 이 FastAPI cached AI answer 예제의 endpoint를 확인해서 tests/test_api_flow.py를 만들어줘.
# 조건:
# 1. test_app_routes.py는 그대로 둔다.
# 2. 실제 Upstash Redis와 Gemini는 호출하지 말고 monkeypatch로 cache_service 함수를 가짜 함수로 바꾼다.
# 3. /ai/answer 성공 흐름과 /ai/answer-cache 삭제 흐름을 테스트한다.
# 4. question query string이 없을 때 422가 나는지도 테스트한다.
# 5. 초보자가 이해할 수 있도록 상단 주석과 테스트 함수 주석을 자세히 넣는다.
# 6. python -m pytest tests로 실행했을 때 통과해야 한다.
#
# 사용 방법:
# 이 파일은 참고 예시입니다. 실제로 실행하고 싶으면 파일명을 test_api_flow.py로 복사하거나 변경합니다.

r"""03_cached-ai-answer-api 핵심 API 흐름 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\03_cached-ai-answer-api
    python -m pytest tests

이 테스트는 실제 Upstash Redis와 Gemini를 호출하지 않습니다.
cache_service 함수를 monkeypatch로 바꾼 뒤,
Gemini 답변 조회와 캐시 삭제 endpoint의 응답 흐름만 확인합니다.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import cache_router
from app.schemas.cache_schema import CachedAnswerResponse


client = TestClient(app)


def test_get_answer_and_clear_cache_flow(monkeypatch) -> None:
    """Gemini 답변을 조회하고 같은 질문의 캐시를 삭제하는 흐름을 확인합니다."""

    monkeypatch.setattr(
        cache_router.cache_service,
        "get_or_create_answer",
        lambda question: CachedAnswerResponse(
            question=question,
            answer="Redis 캐시 설명 Gemini 응답입니다.",
            cached=False,
            ttl_seconds=60,
        ),
    )
    monkeypatch.setattr(cache_router.cache_service, "clear_answer", lambda question: 1)

    answer_response = client.get("/ai/answer", params={"question": "Redis 캐시는 언제 쓰나요?"})
    assert answer_response.status_code == 200
    assert answer_response.json()["cached"] is False
    assert answer_response.json()["ttl_seconds"] == 60

    clear_response = client.delete(
        "/ai/answer-cache",
        params={"question": "Redis 캐시는 언제 쓰나요?"},
    )
    assert clear_response.status_code == 200
    assert clear_response.json()["deleted_count"] == 1


def test_answer_requires_question() -> None:
    """question query string이 없으면 FastAPI가 422 에러를 반환하는지 확인합니다."""

    response = client.get("/ai/answer")

    assert response.status_code == 422
