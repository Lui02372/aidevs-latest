r"""learning_notes 생성 예제입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\03_supabase-db-and-auth\02_supabase-table-and-crud\01_create_learning_note.py
"""

from supabase_client import get_supabase
from zoneinfo import ZoneInfo
from datetime import datetime

def main() -> None:
    """learning_notes 테이블에 메모 1개를 생성합니다."""

    supabase = get_supabase()
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    print(now)
    # insert는 SQL의 INSERT INTO와 비슷합니다.
    # 딕셔너리의 key는 테이블 컬럼명과 같아야 합니다.
    result = (
        supabase.table("learning_notes")
        .insert(
            {
                "id": now.strftime("%Y%m%d%H%M%S%f"),
                "title": "제목",
                "content": "내용",
                "created_at": now.isoformat(),   # timestamptz
            }
        )
        .execute()
    )

    if not result.data:
        raise RuntimeError("insert 결과가 비어 있습니다. learning_notes 테이블과 권한을 확인하세요.")

    # [{}]
   
    created_data = result.data[0]

    print(f"id: {created_data['id']}")
    print(f"title: {created_data['title']}")
    print(f"content: {created_data['content']}")
    print(f"created_at: {created_data['created_at']}")

if __name__ == "__main__":
    main()
