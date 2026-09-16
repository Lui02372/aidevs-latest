"""Supabase Auth와 Bearer token 확인을 담당합니다."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.supabase import get_supabase_client
from app.schemas.auth_schema import (
    AuthenticatedUser,
    AuthRequest,
    AuthResponse,
    SignupRequest,
    UserPublic,
)


# Swagger UI에 Authorize 버튼을 표시하고 Bearer token 입력을 지원합니다.
bearer_security = HTTPBearer(auto_error=False)


def signup(request: SignupRequest) -> UserPublic:
    """이메일/비밀번호로 Supabase Auth 회원가입을 요청합니다."""

    client = get_supabase_client()
    try:
        # 사용자 계정 생성은 FastAPI가 직접 DB에 insert하지 않습니다.
        # Supabase Auth가 auth.users 테이블과 인증 절차를 관리합니다.
        response = client.auth.sign_up(
            {
                "email": request.email,
                "password": request.password,
                # display_name은 auth.users의 raw_user_meta_data에 저장됩니다.
                "options": {"data": {"display_name": request.display_name}},
            }
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"sign up 실패: {error}") from error

    if response.user is None:
        raise HTTPException(status_code=400, detail="user가 없는 signup 응답입니다.")
    return UserPublic(id=response.user.id, email=response.user.email)


def signin(request: AuthRequest) -> AuthResponse:
    """이메일/비밀번호로 로그인하고 Supabase access token을 받습니다."""

    client = get_supabase_client()
    try:
        # 로그인에 성공하면 Supabase가 session과 access_token을 반환합니다.
        # 이 token은 이후 Authorization: Bearer <token> 헤더로 사용합니다.
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
    )
    return AuthResponse(user=user, access_token=response.session.access_token)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_security),
) -> AuthenticatedUser:
    """Swagger 또는 Authorization 헤더의 Bearer token으로 현재 사용자를 확인합니다."""

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization: Bearer <access_token> 헤더가 필요합니다.",
        )

    token = credentials.credentials.strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token 값이 비어 있습니다.",
        )
    client = get_supabase_client()
    try:
        # token 검증은 Supabase Auth에 맡깁니다.
        # 유효한 token이면 response.user에 현재 사용자 정보가 들어옵니다.
        response = client.auth.get_user(token)
    except Exception as error:
        raise HTTPException(status_code=401, detail=f"token 확인 실패: {error}") from error

    if response.user is None:
        raise HTTPException(status_code=401, detail="유효하지 않은 token입니다.")
    return AuthenticatedUser(
        id=response.user.id,
        email=response.user.email,
        access_token=token,
    )


CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]
#age = Annotated[int, Query(ge=0, le=120)]