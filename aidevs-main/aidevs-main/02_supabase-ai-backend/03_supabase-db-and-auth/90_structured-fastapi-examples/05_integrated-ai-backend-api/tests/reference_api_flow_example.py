# 바이브 코딩 프롬프트 예시:
# 이 FastAPI integrated AI backend 예제의 endpoint를 확인해서 tests/test_api_flow.py를 만들어줘.
# 조건:
# 1. test_app_routes.py는 그대로 둔다.
# 2. 실제 Supabase, Redis, Gemini는 호출하지 않는다.
# 3. monkeypatch로 auth_service, chat_service 함수를 가짜 함수로 바꾼다.
# 4. dependency_overrides로 Bearer token 검증을 통과한 가짜 사용자를 만든다.
# 5. /auth/signup, /auth/signin, /chat, /logs 흐름을 테스트한다.
# 6. 인증은 통과했지만 message가 빈 문자열이면 422가 나는지도 테스트한다.
# 7. 초보자가 이해할 수 있도록 상단 주석과 테스트 함수 주석을 자세히 넣는다.
# 8. python -m pytest tests로 실행했을 때 통과해야 한다.
#
# 사용 방법:
# 이 파일은 참고 예시입니다. 실제로 실행하고 싶으면 파일명을 test_api_flow.py로 복사하거나 변경합니다.

r"""05_integrated-ai-backend-api 핵심 API 흐름 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\05_integrated-ai-backend-api
    python -m pytest tests

이 테스트는 실제 Supabase, Redis, Gemini를 호출하지 않습니다.
Auth dependency와 chat_service 함수를 가짜 함수로 바꿔서,
통합 프로젝트의 핵심 endpoint가 연결되어 있는지 확인합니다.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import auth_router, chat_router
from app.schemas.auth_schema import AuthResponse, UserPublic
from app.schemas.chat_schema import ChatLogPublic, ChatResponse
from app.services import auth_service


client = TestClient(app)


def fake_current_user() -> UserPublic:
    """테스트에서 사용할 가짜 로그인 사용자입니다."""

    return UserPublic(id="user-1", email="student@example.com", access_token="test-token")


def test_auth_chat_and_logs_flow(monkeypatch) -> None:
    """회원가입/로그인 후 인증 사용자 기준 채팅과 로그 조회 흐름을 확인합니다."""

    user = UserPublic(id="user-1", email="student@example.com", access_token="test-token")
    auth_response = AuthResponse(user=user, access_token="test-token")
    chat_response = ChatResponse(
        user_message="Redis 캐시는 언제 쓰나요?",
        assistant_message="반복 질문의 응답을 빠르게 돌려줄 때 사용합니다.",
        cached=False,
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=True,
        log_id="log-1",
    )
    log_row = ChatLogPublic(
        id="log-1",
        user_id="user-1",
        user_message="Redis 캐시는 언제 쓰나요?",
        assistant_message="반복 질문의 응답을 빠르게 돌려줄 때 사용합니다.",
        provider="gemini",
        model="gemini-2.5-flash-lite",
        actual_api_called=True,
        cached=False,
        status="success",
        created_at="2026-07-01T00:00:00Z",
    )

    monkeypatch.setattr(auth_router.auth_service, "signup", lambda request: user)
    monkeypatch.setattr(auth_router.auth_service, "signin", lambda request: auth_response)
    monkeypatch.setattr(chat_router.chat_service, "answer_with_cache_and_log", lambda user, request: chat_response)
    monkeypatch.setattr(chat_router.chat_service, "list_logs", lambda access_token: [log_row])
    app.dependency_overrides[auth_service.get_current_user] = fake_current_user

    try:
        signup_response = client.post(
            "/auth/signup",
            json={"email": "student@example.com", "password": "password123"},
        )
        assert signup_response.status_code == 200

        signin_response = client.post(
            "/auth/signin",
            json={"email": "student@example.com", "password": "password123"},
        )
        assert signin_response.status_code == 200
        assert signin_response.json()["token_type"] == "bearer"

        chat_api_response = client.post(
            "/chat",
            headers={"Authorization": "Bearer test-token"},
            json={"message": "Redis 캐시는 언제 쓰나요?"},
        )
        assert chat_api_response.status_code == 200
        assert chat_api_response.json()["provider"] == "gemini"
        assert chat_api_response.json()["actual_api_called"] is True

        logs_response = client.get("/logs", headers={"Authorization": "Bearer test-token"})
        assert logs_response.status_code == 200
        assert logs_response.json()["count"] == 1
    finally:
        app.dependency_overrides.clear()


def test_chat_rejects_empty_message(monkeypatch) -> None:
    """인증은 통과했지만 message가 비어 있으면 422 에러가 나는지 확인합니다."""

    app.dependency_overrides[auth_service.get_current_user] = fake_current_user

    try:
        response = client.post(
            "/chat",
            headers={"Authorization": "Bearer test-token"},
            json={"message": ""},
        )
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()
