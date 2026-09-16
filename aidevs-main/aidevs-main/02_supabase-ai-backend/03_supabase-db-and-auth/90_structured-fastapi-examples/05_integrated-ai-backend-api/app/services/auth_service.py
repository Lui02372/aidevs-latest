"""Supabase Auth와 Bearer token 확인입니다."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.supabase import get_supabase_client
from app.schemas.auth_schema import AuthRequest, AuthResponse, UserPublic


# HTTPBearer를 사용하면 Swagger UI 오른쪽 위에 Authorize 버튼이 생깁니다.
# /auth/signin에서 받은 access_token을 Authorize에 한 번 넣으면,
# Swagger가 /me, /chat, /logs 요청마다 Authorization 헤더를 자동으로 붙여 줍니다.
bearer_security = HTTPBearer(auto_error=False)


def signup(request: AuthRequest) -> UserPublic:
    """Supabase Auth에 회원가입을 요청합니다."""

    client = get_supabase_client()
    try:
        # auth.sign_up은 auth.users에 사용자를 만드는 Supabase Auth 기능입니다.
        # Confirm email 설정이 켜져 있으면 이메일 인증 전까지 로그인에 실패할 수 있습니다.
        response = client.auth.sign_up(
            {"email": request.email, "password": request.password}
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"sign up 실패: {error}") from error
    if response.user is None:
        raise HTTPException(status_code=400, detail="user가 없는 signup 응답입니다.")
    return UserPublic(id=response.user.id, email=response.user.email)


def signin(request: AuthRequest) -> AuthResponse:
    """Supabase Auth에 로그인하고 access token을 받습니다."""

    client = get_supabase_client()
    try:
        # 로그인 성공 시 Supabase는 session을 반환합니다.
        # session.access_token이 이후 Bearer token으로 사용됩니다.
        response = client.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
    except Exception as error:
        raise HTTPException(status_code=401, detail=f"sign in 실패: {error}") from error
    if response.user is None or response.session is None:
        raise HTTPException(status_code=401, detail="로그인 응답에 user/session이 없습니다.")
    user = UserPublic(
        id=response.user.id,
        email=response.user.email,
        access_token=response.session.access_token,
    )
    # access_token은 Swagger Authorize 또는 프론트엔드 session state에 저장해 두고,
    # 보호 API 호출 때마다 Authorization 헤더로 보내는 값입니다.
    return AuthResponse(user=user, access_token=response.session.access_token)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_security),
) -> UserPublic:
    """Bearer token으로 현재 사용자를 확인합니다.

    이전처럼 `authorization: Header(...)`로 직접 받으면 Swagger가 token을
    매번 입력해야 하는 일반 문자열 필드로 보여 줍니다.

    `HTTPBearer`를 사용하면 Swagger의 Authorize 버튼에 token을 한 번 저장하고,
    보호된 endpoint를 이어서 테스트할 수 있습니다.
    """

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Swagger Authorize 또는 Authorization: Bearer <access_token> 헤더가 필요합니다.",
        )

    # HTTPBearer가 "Bearer " 뒤의 실제 token 부분을 credentials에 담아 줍니다.
    token = credentials.credentials.strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token 값이 비어 있습니다.",
        )

    client = get_supabase_client()
    try:
        # token이 유효한지 Supabase Auth에 확인합니다.
        # 유효하면 response.user.id가 현재 로그인한 사용자의 uuid입니다.
        response = client.auth.get_user(token)
    except Exception as error:
        raise HTTPException(status_code=401, detail=f"token 확인 실패: {error}") from error
    if response.user is None:
        raise HTTPException(status_code=401, detail="유효하지 않은 token입니다.")
    return UserPublic(id=response.user.id, email=response.user.email, access_token=token)


CurrentUser = Annotated[UserPublic, Depends(get_current_user)]
