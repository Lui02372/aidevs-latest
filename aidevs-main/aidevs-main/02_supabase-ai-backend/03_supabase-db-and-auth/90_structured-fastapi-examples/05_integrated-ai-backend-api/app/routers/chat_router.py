"""인증된 사용자의 채팅 API입니다."""

from fastapi import APIRouter

from app.schemas.auth_schema import UserPublic
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatLogPublic
from app.services import auth_service, chat_service


# 인증이 필요한 채팅/로그 endpoint를 모은 router입니다.
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    user: auth_service.CurrentUser,
) -> ChatResponse:
    """현재 사용자 기준으로 AI 답변을 만들고 캐시/로그 저장까지 수행합니다."""

    return chat_service.answer_with_cache_and_log(user, request)


@router.get("/logs")
def logs(user: auth_service.CurrentUser) -> dict[str, int | list[ChatLogPublic]]:
    """현재 사용자 token으로 Supabase RLS가 적용된 로그 목록을 조회합니다."""

    data = chat_service.list_logs(user.access_token)
    return {"count": len(data), "data": data}
