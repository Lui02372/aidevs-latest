from pydantic import BaseModel, ConfigDict, Field


class LogCreate(BaseModel):
    """POST /logs가 받는 서비스 로그 생성 요청입니다."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "level": "info",
                    "source": "chat-api",
                    "message": "AI 응답 생성 완료",
                    "request_path": "/chat",
                    "status_code": 200,
                    "latency_ms": 120,
                    "metadata": {"course": "04-mini-project"},
                }
            ]
        }
    )

    level: str = Field(default="info", description="로그 수준. 예: info, warning, error")
    source: str = Field(default="backend", description="로그를 발생시킨 서비스 또는 기능 이름")
    message: str = Field(min_length=1, description="화면에 표시할 로그 메시지")
    request_path: str | None = Field(default="/chat", description="관련 API 경로")
    status_code: int | None = Field(default=200, description="관련 HTTP status code")
    latency_ms: int | None = Field(default=120, description="처리 시간(ms)")
    metadata: dict = Field(default_factory=dict, description="추가로 저장할 JSON 정보")


class LogItem(LogCreate):
    """DB 또는 메모리 저장소에 저장된 로그 응답입니다.

    storage_mode는 이 로그가 실제 Supabase DB에 저장되었는지,
    아니면 수업용 memory fallback에만 저장되었는지 알려 줍니다.
    """

    id: str
    created_at: str
    storage_mode: str = Field(default="unknown", description="저장 위치. supabase 또는 memory")


class LogSummary(BaseModel):
    """level별 로그 개수를 집계한 응답입니다."""

    level: str
    count: int
