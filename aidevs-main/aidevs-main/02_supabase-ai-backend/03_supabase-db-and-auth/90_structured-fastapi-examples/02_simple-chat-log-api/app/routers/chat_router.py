"""채팅 로그 API 경로를 정의합니다."""

import os

from fastapi import APIRouter

import app.core.config  # .env 파일을 읽습니다.
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatLogPublic
from app.services import chat_service


# 채팅 로그와 관련된 endpoint를 한 router에 모읍니다.
router = APIRouter()


@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버 실행 여부와 Supabase/Gemini 환경변수 준비 여부를 확인합니다."""

    return {
        "status": "ok",
        "supabase_configured": bool(os.getenv("SUPABASE_URL"))
        and bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY")),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """사용자 질문을 Gemini로 처리하고 Supabase에 로그를 남깁니다."""

    return chat_service.answer_and_log(request)


@router.get("/logs")
def list_logs() -> dict[str, int | list[ChatLogPublic]]:
    """최근 채팅 로그 목록을 조회합니다."""

    logs = chat_service.list_logs()
    return {"count": len(logs), "data": logs}
