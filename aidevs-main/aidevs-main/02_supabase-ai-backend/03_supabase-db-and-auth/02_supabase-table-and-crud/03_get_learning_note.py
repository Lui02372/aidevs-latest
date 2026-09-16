r"""learning_notes 단건 조회 예제입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\03_supabase-db-and-auth\02_supabase-table-and-crud\03_get_learning_note.py
"""

from supabase_client import get_supabase


def main() -> None:
    """최근 메모 1개의 id를 가져온 뒤, 그 id로 다시 단건 조회합니다."""

    supabase = get_supabase()

    # 먼저 최근 메모 1개를 가져옵니다.
    latest_result = (
        supabase.table("learning_notes")
        .select("*")
        # .select("id,title")
        .eq("id", "20260721140424127812")
        .execute()
    )
    # latest_result = (
    #     supabase.table("learning_notes")
    #     .select("*")
    #     .order("created_at", desc=True)
    #     .limit(1)
    #     .execute()
    # )

    if not latest_result.data:
        print("조회할 메모가 없습니다. 먼저 01_create_learning_note.py를 실행해 보세요.")
        return
    # [{}]
    note = latest_result.data[0]
    print(f"{note["id"]}  {note["title"]} {note["content"]} {note["created_at"]}")

    print("--------------------------------------------------------")
    # eq("id", note_id)는 id가 같은 행 1개만 조회하겠다는 조건입니다.
    
    result = supabase.table("learning_notes").select("*").eq("id", "20260721140424127812").execute()

    # if not result.data:
    #     raise RuntimeError(f"id={note_id} 메모를 다시 조회하지 못했습니다.")

    # note = result.data[0]
    # print("[one learning_note]")
    # print(f"id: {note.get('id')}")
    # print(f"title: {note.get('title')}")
    # print(f"content: {note.get('content')}")
    # print(f"created_at: {note.get('created_at')}")


if __name__ == "__main__":
    main()
