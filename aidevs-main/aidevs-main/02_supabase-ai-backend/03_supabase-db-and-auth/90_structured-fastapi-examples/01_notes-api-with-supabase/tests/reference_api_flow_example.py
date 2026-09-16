# 바이브 코딩 프롬프트 예시:
# 이 FastAPI notes 예제의 endpoint를 확인해서 tests/test_api_flow.py를 만들어줘.
# 조건:
# 1. test_app_routes.py는 그대로 둔다.
# 2. 실제 Supabase는 호출하지 말고 monkeypatch로 notes_service 함수를 가짜 함수로 바꾼다.
# 3. /notes 생성, 목록 조회, 단건 조회, 수정, 삭제 성공 흐름을 테스트한다.
# 4. 존재하지 않는 note_id 조회 404와 빈 title 요청 422도 테스트한다.
# 5. 초보자가 이해할 수 있도록 상단 주석과 테스트 함수 주석을 자세히 넣는다.
# 6. python -m pytest tests로 실행했을 때 통과해야 한다.
#
# 사용 방법:
# 이 파일은 참고 예시입니다. 실제로 실행하고 싶으면 파일명을 test_api_flow.py로 복사하거나 변경합니다.

r"""01_notes-api-with-supabase 핵심 API 흐름 테스트입니다.

실행 방법:
    cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\01_notes-api-with-supabase
    python -m pytest tests

이 테스트는 실제 Supabase를 호출하지 않습니다.
notes_service 함수를 monkeypatch로 가짜 함수로 바꾼 뒤,
FastAPI endpoint가 요청을 받고 응답을 만드는 흐름만 확인합니다.
초보자는 "외부 DB가 없어도 API 모양과 성공/실패 흐름을 테스트할 수 있다"는 점을 보면 됩니다.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import notes_router
from app.schemas.note_schema import NotePublic


client = TestClient(app)


def test_create_list_get_update_delete_note_flow(monkeypatch) -> None:
    """노트 생성, 목록 조회, 단건 조회, 수정, 삭제 endpoint의 기본 흐름을 확인합니다."""

    sample_note = NotePublic(
        id="note-1",
        title="FastAPI 구조",
        content="router, schema, service를 나누어 봅니다.",
        created_at="2026-07-01T00:00:00Z",
    )
    updated_note = NotePublic(
        id="note-1",
        title="수정된 제목",
        content="수정된 내용",
        created_at="2026-07-01T00:00:00Z",
    )

    monkeypatch.setattr(notes_router.notes_service, "create_note", lambda note: sample_note)
    monkeypatch.setattr(notes_router.notes_service, "list_notes", lambda: [sample_note])
    monkeypatch.setattr(notes_router.notes_service, "get_note", lambda note_id: sample_note)
    monkeypatch.setattr(notes_router.notes_service, "update_note", lambda note_id, note: updated_note)
    monkeypatch.setattr(notes_router.notes_service, "delete_note", lambda note_id: True)

    create_response = client.post(
        "/notes",
        json={"title": "FastAPI 구조", "content": "router, schema, service를 나누어 봅니다."},
    )
    assert create_response.status_code == 201
    assert create_response.json()["id"] == "note-1"

    list_response = client.get("/notes")
    assert list_response.status_code == 200
    assert list_response.json()["count"] == 1

    get_response = client.get("/notes/note-1")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "FastAPI 구조"

    update_response = client.put(
        "/notes/note-1",
        json={"title": "수정된 제목", "content": "수정된 내용"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "수정된 제목"

    delete_response = client.delete("/notes/note-1")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "deleted"


def test_get_note_returns_404_when_note_does_not_exist(monkeypatch) -> None:
    """service가 None을 반환하면 API가 404 Not Found로 응답하는지 확인합니다."""

    monkeypatch.setattr(notes_router.notes_service, "get_note", lambda note_id: None)

    response = client.get("/notes/missing-note")

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_create_note_rejects_empty_title() -> None:
    """Pydantic 검증으로 빈 제목 요청이 422 에러가 되는지 확인합니다."""

    response = client.post("/notes", json={"title": "", "content": "내용"})

    assert response.status_code == 422
