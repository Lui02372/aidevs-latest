"""LLM Chat API 경로를 정의하는 파일입니다.

TODO를 채워서 테스트가 통과하도록 완성합니다.
"""

from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatWithHistoryRequest
from app.services import llm_service


router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """TODO: 서버 상태 확인 응답을 완성하세요."""

    return {"status": "TODO"}


@router.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """TODO: single-turn mock 응답을 반환하세요."""

    return llm_service.create_single_turn_response(request)


@router.post("/ai/chat-with-history", response_model=ChatResponse)
def chat_with_history(request: ChatWithHistoryRequest) -> ChatResponse:
    """TODO: 대화 이력을 포함한 multi-turn mock 응답을 반환하세요."""

    return llm_service.create_multi_turn_response(request)
