from pydantic import BaseModel


class ServiceLogItem(BaseModel):
    """서비스 로그 화면에 표시할 로그 한 줄입니다."""

    id: str
    user_email: str | None = None
    action: str
    status: str
    detail: str | None = None
    created_at: str
