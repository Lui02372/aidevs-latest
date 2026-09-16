from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """챗봇 API가 받는 사용자 질문입니다."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "message": "오늘 학습한 Streamlit 상태 관리 내용을 초보자에게 설명해줘."
                }
            ]
        }
    )

    message: str = Field(min_length=1, description="사용자 질문")


class ChatResponse(BaseModel):
    """챗봇 API가 프론트엔드에 반환하는 응답입니다."""

    conversation_id: str
    answer: str
    actual_api_called: bool
    provider: str
    model: str


class ConversationItem(BaseModel):
    """대화 기록 목록에서 한 줄을 표현하는 응답입니다."""

    id: str
    user_email: str
    user_message: str
    assistant_message: str
    created_at: str
