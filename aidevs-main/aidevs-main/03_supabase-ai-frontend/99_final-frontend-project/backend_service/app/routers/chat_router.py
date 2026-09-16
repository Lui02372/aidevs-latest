from fastapi import APIRouter, Depends

from app.core.security import get_bearer_token
from app.schemas.chat_schema import ChatRequest, ChatResponse, ConversationResponse
from app.services.auth_service import get_user_by_token
from app.services.chat_service import create_chat_response, list_conversations


router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat_api(payload: ChatRequest, token: str = Depends(get_bearer_token)) -> dict:
    """로그인한 사용자의 질문을 받아 Gemini 응답을 생성합니다."""

    user = get_user_by_token(token)
    return create_chat_response(user, payload)


@router.get("/conversations", response_model=list[ConversationResponse])
def conversations_api(token: str = Depends(get_bearer_token)) -> list[dict]:
    """로그인한 사용자의 Supabase 대화 기록을 반환합니다."""

    user = get_user_by_token(token)
    return list_conversations(user)
