from fastapi import HTTPException

from app.schemas.auth_schema import SigninRequest, SignupRequest
from app.services.log_service import add_service_log
from app.services.supabase_service import get_auth_client, normalize_user


def signup(payload: SignupRequest) -> dict:
    """Supabase Auth에 새 사용자를 가입시킵니다."""

    client = get_auth_client()

    try:
        # display_name은 Supabase user_metadata에 저장합니다.
        result = client.auth.sign_up(
            {
                "email": payload.email,
                "password": payload.password,
                "options": {"data": {"display_name": payload.display_name}},
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Supabase sign up 실패: {exc}") from exc

    if not result.user:
        raise HTTPException(status_code=400, detail="회원가입 응답에 사용자 정보가 없습니다.")

    user = normalize_user(result.user)
    add_service_log("signup", "success", "회원가입 요청 완료", user)

    return user


def signin(payload: SigninRequest) -> dict:
    """Supabase Auth로 로그인하고 access_token을 반환합니다."""

    client = get_auth_client()

    try:
        result = client.auth.sign_in_with_password(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Supabase sign in 실패: {exc}") from exc

    if not result.user or not result.session:
        raise HTTPException(status_code=401, detail="로그인 응답에 token 정보가 없습니다.")

    user = normalize_user(result.user)
    add_service_log("signin", "success", "로그인 성공", user)

    return {
        "access_token": result.session.access_token,
        "token_type": "bearer",
        "user": user,
    }


def get_user_by_token(token: str) -> dict[str, str]:
    """access_token이 유효한지 Supabase Auth에 확인하고 사용자 정보를 반환합니다."""

    client = get_auth_client()

    try:
        result = client.auth.get_user(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"token 검증 실패: {exc}") from exc

    if not result.user:
        raise HTTPException(status_code=401, detail="유효하지 않은 token입니다.")

    return normalize_user(result.user)


def signout(token: str, user: dict[str, str]) -> dict[str, str]:
    """Supabase Auth 로그아웃을 요청하고 서비스 로그를 남깁니다."""

    client = get_auth_client()

    try:
        # Supabase SDK의 sign_out은 현재 세션을 기준으로 동작하므로,
        # 요청받은 token을 세션처럼 설정한 뒤 로그아웃을 시도합니다.
        client.auth.set_session(token, token)
        client.auth.sign_out()
    except Exception:
        pass

    add_service_log("signout", "success", "로그아웃 요청 완료", user)
    return {"message": "로그아웃되었습니다."}
