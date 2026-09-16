from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """Gemini에 전달할 사용자 질문 요청입니다."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "message": "내 대화 이력을 바탕으로 오늘 학습한 내용을 세 줄로 요약해줘."
                }
            ]
        }
    )

    message: str = Field(min_length=1, max_length=1000, description="Gemini에 전달할 사용자 질문")


class ChatResponse(BaseModel):
    """AI 응답 생성 결과입니다."""

    answer: str
    provider: str
    model: str
    actual_api_called: bool


class ConversationResponse(BaseModel):
    """Supabase에 저장된 대화 기록 한 줄입니다."""

    id: str
    user_message: str
    assistant_message: str
    provider: str
    model: str | None = None
    created_at: str | None = None
