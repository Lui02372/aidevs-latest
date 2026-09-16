from fastapi import HTTPException

from app.services.supabase_service import get_service_client


def _schema_error_message(table_name: str) -> str:
    """Supabase 테이블이 없을 때 수강생에게 보여 줄 안내 메시지를 만듭니다."""

    return (
        f"Supabase 테이블 '{table_name}'을 찾을 수 없습니다. "
        "backend_service/schema.sql을 Supabase SQL Editor에서 먼저 실행하세요."
    )


def add_service_log(
    action: str,
    status: str,
    message: str,
    user: dict[str, str] | None = None,
) -> None:
    """서비스 이벤트를 Supabase 로그 테이블에 저장합니다.

    로그 저장은 부가 기능입니다. 따라서 로그 테이블이 아직 없더라도
    회원가입/로그인 같은 핵심 API가 실패하지 않도록 오류를 삼킵니다.
    """

    row = {
        "action": action,
        "status": status,
        "message": message,
        "user_id": user["id"] if user else None,
        "user_email": user["email"] if user else None,
    }

    try:
        get_service_client().table("frontend_service_logs").insert(row).execute()
    except Exception:
        # 수업 중 schema.sql 실행 전에도 로그인 흐름은 먼저 확인할 수 있게 합니다.
        return


def list_service_logs(user: dict[str, str]) -> list[dict]:
    """현재 사용자의 최근 서비스 로그를 Supabase에서 조회합니다."""

    try:
        result = (
            get_service_client()
            .table("frontend_service_logs")
            .select("id, action, status, message, created_at")
            .eq("user_id", user["id"])
            .order("created_at", desc=True)
            .limit(50)
            .execute()
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=_schema_error_message("frontend_service_logs")) from exc

    return result.data or []
