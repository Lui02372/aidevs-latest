# 바이브 코딩 프롬프트 예시:
# 이 FastAPI auth/jwt/profile 예제의 endpoint를 확인해서 tests/test_api_flow.py를 만들어줘.
# 조건:
# 1. test_app_routes.py는 그대로 둔다.
# 2. 실제 Supabase Auth와 RLS 테이블은 호출하지 않는다.
# 3. monkeypatch로 auth_service, profile_service 함수를 가짜 함수로 바꾼다.
# 4. dependency_overrides로 Bearer token 검증을 통과한 가짜 사용자를 만든다.
# 5. /auth/signup, /auth/signin, /me, /profile 조회/수정 흐름을 테스트한다.
# 6. Authorization header가 없을 때 /me가 401을 반환하는지도 테스트한다.
# 7. 초보자가 이해할 수 있도록 상단 주석과 테스트 함수 주석을 자세히 넣는다.
# 8. python -m pytest tests로 실행했을 때 통과해야 한다.
#
# 사용 방법:
# 이 파일은 참고 예시입니다. 실제로 실행하고 싶으면 파일명을 test_api_flow.py로 복사하거나 변경합니다.

r"""04_auth-jwt-profile-api 핵심 API 흐름 테스트입니다.

실행 방법:
    cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\04_auth-jwt-profile-api
    python -m pytest tests

이 테스트는 실제 Supabase Auth나 RLS 테이블을 호출하지 않습니다.
회원가입/로그인 service와 Bearer token 검증 dependency를 가짜 함수로 바꿔서,
Auth/Profile endpoint가 어떻게 연결되는지 확인합니다.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import auth_router, profile_router
from app.schemas.auth_schema import AuthResponse, UserPublic
from app.schemas.profile_schema import ProfilePublic
from app.services import auth_service


client = TestClient(app)


def fake_current_user() -> UserPublic:
    """테스트에서 사용할 가짜 로그인 사용자입니다."""

    return UserPublic(id="user-1", email="student@example.com", access_token="test-token")


def test_signup_signin_me_and_profile_flow(monkeypatch) -> None:
    """회원가입, 로그인, 내 정보 조회, 프로필 조회/수정 흐름을 확인합니다."""

    user = UserPublic(id="user-1", email="student@example.com", access_token="test-token")
    auth_response = AuthResponse(user=user, access_token="test-token")
    profile = ProfilePublic(id="user-1", display_name="홍길동")

    monkeypatch.setattr(auth_router.auth_service, "signup", lambda request: user)
    monkeypatch.setattr(auth_router.auth_service, "signin", lambda request: auth_response)
    monkeypatch.setattr(profile_router.profile_service, "get_profile", lambda access_token: profile)
    monkeypatch.setattr(
        profile_router.profile_service,
        "upsert_profile",
        lambda user_id, access_token, request: ProfilePublic(
            id=user_id,
            display_name=request.display_name,
        ),
    )
    app.dependency_overrides[auth_service.get_current_user] = fake_current_user

    try:
        signup_response = client.post(
            "/auth/signup",
            json={"email": "student@example.com", "password": "password123"},
        )
        assert signup_response.status_code == 200
        assert signup_response.json()["id"] == "user-1"

        signin_response = client.post(
            "/auth/signin",
            json={"email": "student@example.com", "password": "password123"},
        )
        assert signin_response.status_code == 200
        assert signin_response.json()["access_token"] == "test-token"

        me_response = client.get("/me", headers={"Authorization": "Bearer test-token"})
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "student@example.com"

        profile_response = client.get("/profile", headers={"Authorization": "Bearer test-token"})
        assert profile_response.status_code == 200
        assert profile_response.json()["display_name"] == "홍길동"

        update_response = client.put(
            "/profile",
            headers={"Authorization": "Bearer test-token"},
            json={"display_name": "김코딩"},
        )
        assert update_response.status_code == 200
        assert update_response.json()["display_name"] == "김코딩"
    finally:
        app.dependency_overrides.clear()


def test_me_requires_bearer_token() -> None:
    """dependency override가 없을 때 /me는 Bearer token 없이는 401을 반환합니다."""

    app.dependency_overrides.clear()

    response = client.get("/me")

    assert response.status_code == 401
