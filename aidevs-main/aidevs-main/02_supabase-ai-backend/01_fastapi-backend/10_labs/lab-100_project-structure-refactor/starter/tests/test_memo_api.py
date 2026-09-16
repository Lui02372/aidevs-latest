from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_memos_excludes_internal_note():
    response = client.get("/memos")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert "internal_note" not in body["data"][0]


def test_create_memo():
    response = client.post(
        "/memos",
        json={
            "title": "새 메모",
            "content": "구조 분리 실습입니다.",
            "tags": ["lab"],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 1
    assert body["title"] == "새 메모"
