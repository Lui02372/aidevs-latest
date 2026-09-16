from pydantic import BaseModel, ConfigDict, Field


class SignupRequest(BaseModel):
    """회원가입 API가 받는 요청 데이터입니다."""

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

    email: str = Field(min_length=3, description="로그인에 사용할 이메일")
    password: str = Field(min_length=4, description="수업용 비밀번호")
    display_name: str = Field(min_length=1, description="화면에 표시할 이름")


class SigninRequest(BaseModel):
    """로그인 API가 받는 요청 데이터입니다."""

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

    email: str = Field(min_length=3, description="회원가입 때 사용한 이메일")
    password: str = Field(min_length=4, description="회원가입 때 사용한 비밀번호")


class UserResponse(BaseModel):
    """프론트엔드에 보여 줄 사용자 정보 응답입니다."""

    email: str
    display_name: str


class AuthResponse(BaseModel):
    """로그인 성공 시 반환하는 token과 사용자 정보입니다."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    """간단한 성공 메시지를 반환할 때 사용하는 응답입니다."""

    message: str
