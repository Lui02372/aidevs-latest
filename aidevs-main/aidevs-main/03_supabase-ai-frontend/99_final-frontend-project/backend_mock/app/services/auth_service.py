from fastapi import HTTPException, status

from app.core.security import create_access_token
from app.schemas.auth_schema import SigninRequest, SignupRequest
from app.services.log_service import add_log
from app.services.memory_store import sessions, users


def signup(payload: SignupRequest) -> dict:
    """회원가입 요청을 메모리 users 딕셔너리에 저장합니다.

    mock backend에서는 비밀번호 암호화나 이메일 인증을 하지 않습니다.
    프론트엔드가 회원가입 API 호출 흐름을 연습할 수 있도록 최소 기능만 제공합니다.
    """

    email = payload.email.lower().strip()
    if email in users:
        add_log("signup", "failed", "이미 가입된 이메일", email)
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    users[email] = {
        "email": email,
        "password": payload.password,
        "display_name": payload.display_name,
    }
    add_log("signup", "success", "회원가입 완료", email)
    return {"email": email, "display_name": payload.display_name}


def signin(payload: SigninRequest) -> dict:
    """이메일과 비밀번호를 확인하고 mock access token을 발급합니다."""

    email = payload.email.lower().strip()
    user = users.get(email)
    if user is None or user["password"] != payload.password:
        add_log("signin", "failed", "이메일 또는 비밀번호 불일치", email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        )

    token = create_access_token()

    # token과 email의 관계를 저장해 두면 이후 /me, /chat 같은 보호 API에서
    # "이 token은 누구의 token인가?"를 확인할 수 있습니다.
    sessions[token] = email
    add_log("signin", "success", "로그인 성공", email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": user["email"],
            "display_name": user["display_name"],
        },
    }


def get_user_by_token(token: str) -> dict:
    """access token으로 현재 사용자를 찾습니다."""

    email = sessions.get(token)
    if not email or email not in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 token입니다.",
        )

    user = users[email]
    return {
        "email": user["email"],
        "display_name": user["display_name"],
    }


def signout(token: str) -> dict:
    """현재 token을 세션 저장소에서 제거해 로그아웃 처리합니다."""

    email = sessions.pop(token, None)
    if email:
        add_log("signout", "success", "로그아웃 완료", email)
    return {"message": "로그아웃되었습니다."}
