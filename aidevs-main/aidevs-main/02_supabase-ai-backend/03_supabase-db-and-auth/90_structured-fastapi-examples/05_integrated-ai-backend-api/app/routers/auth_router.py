"""Auth와 상태 확인 API입니다."""

import os

from fastapi import APIRouter

import app.core.config  # .env 파일을 읽습니다.
from app.schemas.auth_schema import AuthRequest, AuthResponse, UserPublic
from app.services import auth_service


# 통합 예제의 인증 endpoint를 모은 router입니다.
router = APIRouter()


@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버 실행 여부와 Supabase/Redis/Gemini 환경변수 준비 상태를 확인합니다."""

    return {
        "status": "ok",
        "supabase_configured": bool(os.getenv("SUPABASE_URL"))
        and bool(os.getenv("SUPABASE_ANON_KEY"))
        and bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY")),
        "redis_configured": bool(os.getenv("UPSTASH_REDIS_REST_URL"))
        and bool(os.getenv("UPSTASH_REDIS_REST_TOKEN")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


@router.post("/auth/signup", response_model=UserPublic)
def signup(request: AuthRequest) -> UserPublic:
    """Supabase Auth 회원가입을 요청합니다."""

    return auth_service.signup(request)


@router.post("/auth/signin", response_model=AuthResponse)
def signin(request: AuthRequest) -> AuthResponse:
    """Supabase Auth 로그인 후 access token을 반환합니다."""

    return auth_service.signin(request)


@router.get("/me", response_model=UserPublic)
def me(user: auth_service.CurrentUser) -> UserPublic:
    """Swagger Authorize에 넣은 token이 가리키는 현재 사용자를 반환합니다."""

    return user
