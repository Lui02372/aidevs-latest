from fastapi import APIRouter, Depends

from app.core.security import get_bearer_token
from app.schemas.auth_schema import (
    AuthResponse,
    MessageResponse,
    SigninRequest,
    SignupRequest,
    UserResponse,
)
from app.services.auth_service import get_user_by_token, signin, signout, signup


router = APIRouter(tags=["auth"])


@router.post("/auth/signup", response_model=UserResponse)
def signup_endpoint(payload: SignupRequest) -> dict:
    """회원가입 요청을 auth_service로 전달합니다."""

    return signup(payload)


@router.post("/auth/signin", response_model=AuthResponse)
def signin_endpoint(payload: SigninRequest) -> dict:
    """로그인 요청을 처리하고 access_token을 반환합니다."""

    return signin(payload)


@router.post("/auth/signout", response_model=MessageResponse)
def signout_endpoint(token: str = Depends(get_bearer_token)) -> dict:
    """Authorization header에서 token을 꺼낸 뒤 로그아웃 처리합니다."""

    return signout(token)


@router.get("/me", response_model=UserResponse)
def me_endpoint(token: str = Depends(get_bearer_token)) -> dict:
    """현재 token이 가리키는 사용자 정보를 반환합니다."""

    return get_user_by_token(token)
