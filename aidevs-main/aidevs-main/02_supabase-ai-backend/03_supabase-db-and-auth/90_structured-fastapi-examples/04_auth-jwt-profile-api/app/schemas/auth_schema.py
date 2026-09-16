"""Auth 요청/응답 모델입니다."""

from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    """로그인 요청 Body입니다."""

    email: str = Field(min_length=3, examples=["student@example.com"])
    password: str = Field(min_length=6, examples=["password123"])


class SignupRequest(AuthRequest):
    """회원가입 시 이메일/비밀번호와 함께 받을 사용자 표시 이름입니다."""

    display_name: str = Field(min_length=1, max_length=50, examples=["수강생"])


class UserPublic(BaseModel):
    """API 응답에서 보여 줄 사용자 정보입니다."""

    id: str
    email: str | None = None


class AuthenticatedUser(UserPublic):
    """서버 내부에서만 Bearer token을 함께 사용하는 인증 사용자입니다."""

    access_token: str | None = None


class AuthResponse(BaseModel):
    """로그인 성공 응답입니다."""

    user: UserPublic
    access_token: str
    token_type: str = "bearer"
