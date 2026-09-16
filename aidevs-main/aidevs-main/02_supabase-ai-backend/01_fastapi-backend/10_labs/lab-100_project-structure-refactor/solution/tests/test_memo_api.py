r"""구조 분리된 메모 API 테스트입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-100_project-structure-refactor\solution
    python -m pytest -s

이 테스트는 uvicorn 서버를 직접 실행하지 않고 TestClient로 app.main의 FastAPI 앱을 호출합니다.
`-s` 옵션을 붙이면 print로 출력한 진행 과정도 터미널에서 볼 수 있습니다.
"""

from fastapi.testclient import TestClient

from app.main import app


# TestClient는 브라우저나 Postman 대신 코드에서 API를 호출하는 테스트 도구입니다.
client = TestClient(app)


def test_health_check():
    print("1. GET /health 상태 확인 API를 호출합니다.")
    response = client.get("/health")

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_memos_excludes_internal_note():
    print("2. GET /memos 메모 목록 API를 호출합니다.")
    response = client.get("/memos")

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert "internal_note" not in body["data"][0]


def test_search_memos():
    print("3. GET /memos/search 검색 API를 호출합니다.")
    response = client.get("/memos/search", params={"keyword": "구조"})

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert "구조" in body["data"][0]["title"] or "구조" in body["data"][0]["content"]


def test_get_missing_memo_returns_404():
    print("4. GET /memos/999 없는 메모 조회 API를 호출합니다.")
    response = client.get("/memos/999")

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 404


def test_create_memo():
    print("5. POST /memos 새 메모 생성 API를 호출합니다.")
    response = client.post(
        "/memos",
        json={
            "title": "새 메모",
            "content": "구조 분리 실습입니다.",
            "tags": ["lab"],
        },
    )

    print("   응답:", response.status_code, response.json())
    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 1
    assert body["title"] == "새 메모"
