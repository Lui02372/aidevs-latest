r"""learning_notes CRUD 통합 예제입니다.

01~05에서 나누어 본 생성/조회/수정/삭제 흐름을 한 번에 실행합니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\03_supabase-db-and-auth\02_supabase-table-and-crud\06_learning_notes_crud_all.py
"""

from supabase import Client

from supabase_client import get_supabase


def create_note(supabase: Client) -> dict:
    """learning_notes 테이블에 실습용 메모를 1개 저장합니다."""

    result = (
        supabase.table("learning_notes")
        .insert(
            {
                "title": "Supabase CRUD practice",
                "content": "Python에서 insert, select, update, delete를 차례대로 실행합니다.",
            }
        )
        .execute()
    )

    if not result.data:
        raise RuntimeError("insert 결과가 비어 있습니다. learning_notes 테이블과 권한을 확인하세요.")

    return result.data[0]


def list_recent_notes(supabase: Client) -> list[dict]:
    """최근 학습 메모 5개를 조회합니다."""

    result = (
        supabase.table("learning_notes")
        .select("*")
        .order("created_at", desc=True)
        .limit(5)
        .execute()
    )

    return result.data


def get_note(supabase: Client, note_id: str) -> dict:
    """id 조건으로 메모 1개를 조회합니다."""

    result = supabase.table("learning_notes").select("*").eq("id", note_id).execute()
    if not result.data:
        raise RuntimeError(f"id={note_id} 메모를 조회하지 못했습니다.")

    return result.data[0]


def update_note_title(supabase: Client, note_id: str) -> dict:
    """방금 만든 실습 메모의 제목을 수정합니다."""

    result = (
        supabase.table("learning_notes")
        .update({"title": "Supabase CRUD practice - updated"})
        .eq("id", note_id)
        .execute()
    )

    if not result.data:
        raise RuntimeError("update 결과가 비어 있습니다. note_id와 테이블 권한을 확인하세요.")

    return result.data[0]


def delete_note(supabase: Client, note_id: str) -> None:
    """실습으로 만든 메모를 삭제합니다."""

    supabase.table("learning_notes").delete().eq("id", note_id).execute()


def print_note(label: str, note: dict) -> None:
    """메모 한 개를 보기 좋게 출력합니다."""

    print(f"\n[{label}]")
    print(f"id: {note.get('id')}")
    print(f"title: {note.get('title')}")
    print(f"content: {note.get('content')}")
    print(f"created_at: {note.get('created_at')}")


def main() -> None:
    """CRUD 흐름을 create -> list -> get -> update -> delete 순서로 실행합니다."""

    supabase = get_supabase()

    created = create_note(supabase)
    print_note("created note", created)

    notes = list_recent_notes(supabase)
    print("\n[recent notes]")
    for index, note in enumerate(notes, start=1):
        print(f"{index}. {note.get('title')} - {note.get('content')}")

    selected = get_note(supabase, created["id"])
    print_note("selected note", selected)

    updated = update_note_title(supabase, created["id"])
    print_note("updated note", updated)

    delete_note(supabase, created["id"])
    print(f"\n[deleted practice note]\n{created['id']}")

    print("\nResult: insert/select/update/delete 흐름을 모두 실행했습니다.")


if __name__ == "__main__":
    main()
