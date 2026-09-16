from fastapi import APIRouter, Depends

from app.core.security import get_bearer_token
from app.schemas.auth_schema import AuthResponse, SigninRequest, SignupRequest, UserResponse
from app.services.auth_service import get_user_by_token, signin, signout, signup


router = APIRouter(tags=["auth"])


@router.post("/auth/signup", response_model=UserResponse)
def signup_api(payload: SignupRequest) -> dict:
    """회원가입 요청을 Supabase Auth service 함수로 전달합니다."""

    return signup(payload)


@router.post("/auth/signin", response_model=AuthResponse)
def signin_api(payload: SigninRequest) -> dict:
    """로그인 요청을 처리하고 Supabase access_token을 반환합니다."""

    return signin(payload)


@router.post("/auth/signout")
def signout_api(token: str = Depends(get_bearer_token)) -> dict[str, str]:
    """Authorization header의 token으로 현재 사용자를 확인한 뒤 로그아웃합니다."""

    user = get_user_by_token(token)
    return signout(token, user)


@router.get("/me", response_model=UserResponse)
def me_api(token: str = Depends(get_bearer_token)) -> dict[str, str]:
    """현재 access_token에 해당하는 Supabase 사용자 정보를 반환합니다."""

    return get_user_by_token(token)
