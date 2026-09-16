"""멀티턴 채팅 API 경로입니다."""

import os

from fastapi import APIRouter

import app.core.config  # .env 파일을 읽습니다.
from app.schemas.chat_schema import ChatMessage, ChatRequest, ChatResponse
from app.services import chat_service


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버와 필수 환경변수 준비 상태를 확인합니다."""

    return {
        "status": "ok",
        "supabase_configured": bool(os.getenv("SUPABASE_URL"))
        and bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """이전 대화를 문맥으로 사용해 새 답변을 만듭니다."""

    return chat_service.chat(request)


@router.get("/conversations/{conversation_id}/messages", response_model=list[ChatMessage])
def messages(conversation_id: str) -> list[ChatMessage]:
    """특정 대화의 전체 이력을 조회합니다."""

    return chat_service.list_messages(conversation_id)
