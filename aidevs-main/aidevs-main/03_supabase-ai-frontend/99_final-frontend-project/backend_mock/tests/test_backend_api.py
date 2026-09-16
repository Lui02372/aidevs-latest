from fastapi.testclient import TestClient

from app.main import app
from app.services.memory_store import reset_store


def test_auth_chat_log_flow():
    """회원가입부터 로그아웃까지 프론트엔드가 사용할 핵심 API 흐름을 확인합니다."""

    # 메모리 저장소를 사용하는 mock backend는 이전 테스트 데이터가 남을 수 있으므로
    # 테스트 시작 전에 항상 깨끗하게 비웁니다.
    reset_store()
    client = TestClient(app)

    # 1. 서버가 켜져 있는지 확인합니다.
    health = client.get("/health")
    assert health.status_code == 200

    # 2. 수업용 계정을 회원가입합니다.
    signup = client.post(
        "/auth/signup",
        json={
            "email": "student@example.com",
            "password": "pass1234",
            "display_name": "수강생",
        },
    )
    assert signup.status_code == 200

    # 3. 로그인 후 access_token을 받습니다.
    signin = client.post(
        "/auth/signin",
        json={
            "email": "student@example.com",
            "password": "pass1234",
        },
    )
    assert signin.status_code == 200
    token = signin.json()["access_token"]

    # 4. 보호된 API는 Authorization: Bearer <token> header가 필요합니다.
    headers = {"Authorization": f"Bearer {token}"}

    # 5. 현재 사용자 정보, 채팅, 대화 기록, 서비스 로그 API를 순서대로 확인합니다.
    me = client.get("/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "student@example.com"

    chat = client.post("/chat", headers=headers, json={"message": "오늘 배운 내용을 요약해줘"})
    assert chat.status_code == 200
    assert chat.json()["actual_api_called"] is False

    conversations = client.get("/conversations", headers=headers)
    assert conversations.status_code == 200
    assert len(conversations.json()) == 1

    logs = client.get("/service-logs", headers=headers)
    assert logs.status_code == 200
    assert len(logs.json()) >= 3

    signout = client.post("/auth/signout", headers=headers)
    assert signout.status_code == 200
