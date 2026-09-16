"""Auth 관련 API 경로입니다."""

import os

from fastapi import APIRouter

import app.core.config  # .env 파일을 읽습니다.
from app.schemas.auth_schema import AuthRequest, AuthResponse, SignupRequest, UserPublic
from app.services import auth_service


# 인증 관련 endpoint를 모은 router입니다.
router = APIRouter()


@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버 실행 여부와 Supabase Auth 환경변수 준비 상태를 확인합니다."""

    return {
        "status": "ok",
        "supabase_configured": bool(os.getenv("SUPABASE_URL"))
        and bool(os.getenv("SUPABASE_ANON_KEY"))
        and bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY")),
    }


@router.post("/auth/signup", response_model=UserPublic)
def signup(request: SignupRequest) -> UserPublic:
    """Supabase Auth에 회원가입을 요청합니다."""

    return auth_service.signup(request)


@router.post("/auth/signin", response_model=AuthResponse)
def signin(request: AuthRequest) -> AuthResponse:
    """Supabase Auth에 로그인하고 access token을 반환합니다."""

    return auth_service.signin(request)


@router.get("/me", response_model=UserPublic)
def me(user: auth_service.CurrentUser) -> UserPublic:
    """Authorization Bearer token으로 확인된 현재 사용자 정보를 반환합니다."""

    return user
