"""Profile 요청/응답 모델입니다.

Profile API에서는 로그인한 사용자의 화면 표시 이름을 저장하고 조회합니다.
"""

from pydantic import BaseModel, Field


class ProfileUpdate(BaseModel):
    """PUT /profile 요청 Body입니다."""

    # display_name은 화면에 보여 줄 이름입니다.
    # 로그인 email과 별도로 사용자에게 보여 줄 이름을 저장한다고 보면 됩니다.
    display_name: str = Field(min_length=1, examples=["홍길동"])


class ProfilePublic(BaseModel):
    """클라이언트에 반환하는 프로필 응답 모델입니다."""

    id: str
    display_name: str
    created_at: str | None = None
    updated_at: str | None = None
