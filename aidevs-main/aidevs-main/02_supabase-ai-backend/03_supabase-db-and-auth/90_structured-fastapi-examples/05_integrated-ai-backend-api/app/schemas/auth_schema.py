"""Auth 모델입니다."""

from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    """회원가입과 로그인 요청 Body입니다."""

    email: str = Field(min_length=3, examples=["student@example.com"])
    password: str = Field(min_length=6, examples=["password123"])


class UserPublic(BaseModel):
    """클라이언트에 공개할 사용자 정보입니다."""

    id: str
    email: str | None = None
    # access_token은 보호 API 호출에 필요한 값입니다.
    # Swagger Authorize에 이 값을 넣으면 /me, /chat, /logs를 이어서 테스트할 수 있습니다.
    access_token: str | None = None


class AuthResponse(BaseModel):
    """로그인 성공 응답입니다."""

    user: UserPublic
    access_token: str
    token_type: str = "bearer"
