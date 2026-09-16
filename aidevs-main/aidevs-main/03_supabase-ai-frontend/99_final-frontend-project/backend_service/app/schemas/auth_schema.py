from pydantic import BaseModel, ConfigDict, Field


class SignupRequest(BaseModel):
    """Supabase Auth 회원가입 API가 받는 요청 데이터입니다."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "student@example.com",
                    "password": "pass1234",
                    "display_name": "수강생",
                }
            ]
        }
    )

    email: str = Field(min_length=3, description="Supabase Auth에 가입할 이메일")
    password: str = Field(min_length=6, description="Supabase Auth 로그인 비밀번호")
    display_name: str = Field(min_length=1, max_length=50, description="화면에 표시할 이름")


class SigninRequest(BaseModel):
    """Supabase Auth 로그인 API가 받는 요청 데이터입니다."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "student@example.com",
                    "password": "pass1234",
                }
            ]
        }
    )

    email: str = Field(min_length=3, description="Supabase Auth에 가입한 이메일")
    password: str = Field(min_length=1, description="Supabase Auth 로그인 비밀번호")


class UserResponse(BaseModel):
    """프론트엔드에 반환할 사용자 정보입니다."""

    id: str
    email: str
    display_name: str


class AuthResponse(BaseModel):
    """로그인 성공 시 Supabase access_token과 사용자 정보를 함께 반환합니다."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
