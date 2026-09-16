"""LLM Chat API 경로를 정의하는 solution 파일입니다."""

from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatWithHistoryRequest
from app.services import llm_service


router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """서버 상태 확인 응답을 반환합니다."""

    return {"status": "ok"}


@router.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """single-turn mock 응답을 반환합니다."""

    return llm_service.create_single_turn_response(request)


@router.post("/ai/chat-with-history", response_model=ChatResponse)
def chat_with_history(request: ChatWithHistoryRequest) -> ChatResponse:
    """대화 이력을 포함한 multi-turn mock 응답을 반환합니다."""

    return llm_service.create_multi_turn_response(request)
