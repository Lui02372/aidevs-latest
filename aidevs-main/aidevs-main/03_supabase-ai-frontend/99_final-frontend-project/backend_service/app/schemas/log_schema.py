from pydantic import BaseModel


class ServiceLogResponse(BaseModel):
    """운영 로그 화면에 표시할 서비스 로그 한 줄입니다."""

    id: str
    action: str
    status: str
    message: str | None = None
    created_at: str | None = None
