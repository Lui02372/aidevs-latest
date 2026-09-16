from fastapi import HTTPException

from app.core.config import (
    SUPABASE_ANON_KEY,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_URL,
)


def _require_supabase_package():
    """supabase 패키지를 늦게 import하고, 없으면 이해하기 쉬운 오류를 반환합니다."""

    try:
        from supabase import create_client
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="supabase 패키지가 설치되어 있지 않습니다. pip install -r requirements.txt를 실행하세요.",
        ) from exc

    return create_client


def get_auth_client():
    """Supabase Auth용 client를 만듭니다.

    회원가입, 로그인, token 검증처럼 사용자 인증과 관련된 작업에는 anon key를 사용합니다.
    """

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL 또는 SUPABASE_ANON_KEY가 설정되어 있지 않습니다.",
        )

    create_client = _require_supabase_package()
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def get_service_client():
    """Supabase DB 접근용 service role client를 만듭니다.

    service role key는 강한 권한을 가진 서버 전용 key입니다.
    프론트엔드나 GitHub에 노출하면 안 되며, 백엔드 .env에만 저장합니다.
    """

    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL 또는 SUPABASE_SERVICE_ROLE_KEY가 설정되어 있지 않습니다.",
        )

    create_client = _require_supabase_package()
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def normalize_user(user) -> dict[str, str]:
    """Supabase user 객체를 프론트엔드가 쓰기 쉬운 dict로 변환합니다."""

    metadata = getattr(user, "user_metadata", None) or {}
    return {
        "id": str(user.id),
        "email": user.email,
        "display_name": metadata.get("display_name") or user.email,
    }
