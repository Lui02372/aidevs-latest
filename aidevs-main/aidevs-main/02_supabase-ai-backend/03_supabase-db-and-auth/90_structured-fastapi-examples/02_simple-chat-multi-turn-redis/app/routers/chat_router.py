"""Redis 멀티턴 채팅 API 경로입니다."""

import os

from fastapi import APIRouter

import app.core.config  # .env 파일을 읽습니다.
from app.schemas.chat_schema import ChatRequest, ChatResponse, ConversationMessage
from app.services import chat_service


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "redis_configured": bool(os.getenv("UPSTASH_REDIS_REST_URL"))
        and bool(os.getenv("UPSTASH_REDIS_REST_TOKEN")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return chat_service.chat(request)


@router.get("/conversations/{conversation_id}/messages", response_model=list[ConversationMessage])
def messages(conversation_id: str) -> list[ConversationMessage]:
    return chat_service.get_messages(conversation_id)


@router.delete("/conversations/{conversation_id}")
def clear_conversation(conversation_id: str) -> dict[str, int | str]:
    return {
        "conversation_id": conversation_id,
        "deleted_count": chat_service.clear_conversation(conversation_id),
    }
