"""FastAPI TestClient 예제.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
    python 05_simple-test-client.py

TestClient는 실제 서버를 uvicorn으로 띄우지 않고도 API를 호출해 볼 수 있게 해줍니다.
초보자는 먼저 "API를 코드로 테스트할 수 있다"는 개념을 이해하면 됩니다.
"""

# TestClient는 FastAPI 앱을 코드 안에서 직접 호출하는 테스트 도구입니다.
# 브라우저나 Postman으로 직접 누르지 않고도 API 응답을 확인할 수 있습니다.
from fastapi.testclient import TestClient

# app_for_test.py 파일 안의 app 객체를 가져옵니다.
# 이 app을 TestClient에 넣어 테스트합니다.
from app_for_test import app


# TestClient는 브라우저나 Postman 대신 API를 호출해 주는 테스트 도구입니다.
client = TestClient(app)


def test_health_check():
    """GET /health가 정상 응답하는지 확인합니다."""

    # 실제 HTTP 요청처럼 보이지만, uvicorn 서버를 따로 켜지 않아도 됩니다.
    response = client.get("/health")

    # response.status_code는 HTTP 상태 코드입니다. 정상 응답이면 보통 200입니다.
    # response.json()은 응답 JSON을 Python dict로 바꿔 줍니다.
    print("GET /health")
    print("status_code:", response.status_code)
    print("json:", response.json())


def test_create_message():
    """POST /messages가 요청 body를 처리하는지 확인합니다."""

    # json=... 인자에 dict를 넣으면 TestClient가 JSON Request Body로 보내 줍니다.
    response = client.post("/messages", json={"text": "hello fastapi"})

    print("\nPOST /messages")
    print("status_code:", response.status_code)
    print("json:", response.json())


if __name__ == "__main__":
    # 이 파일을 직접 실행하면 아래 두 함수를 순서대로 호출합니다.
    # pytest를 아직 배우지 않았어도 테스트 흐름을 눈으로 확인할 수 있습니다.
    test_health_check()
    test_create_message()
