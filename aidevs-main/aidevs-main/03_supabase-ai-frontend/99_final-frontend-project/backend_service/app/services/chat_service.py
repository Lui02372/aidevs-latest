from fastapi import HTTPException

from app.schemas.chat_schema import ChatRequest
from app.services.cache_service import get_cached_answer, make_cache_key, set_cached_answer
from app.services.gemini_service import generate_ai_answer
from app.services.log_service import add_service_log
from app.services.supabase_service import get_service_client


def create_chat_response(user: dict[str, str], payload: ChatRequest) -> dict:
    """사용자 질문에 답하고 Supabase에 대화 기록을 저장합니다.

    흐름:
    1. Redis 캐시에서 같은 질문의 답변을 찾습니다.
    2. 캐시가 없으면 Gemini API를 호출합니다.
    3. 답변을 Supabase 테이블에 저장합니다.
    4. 프론트엔드에 답변 정보를 반환합니다.
    """

    cache_key = make_cache_key(user["id"], payload.message)
    cached_answer = get_cached_answer(cache_key)

    if cached_answer:
        # 캐시된 답변이 있으면 Gemini를 다시 호출하지 않습니다.
        ai_result = {
            "answer": cached_answer,
            "provider": "upstash-cache",
            "model": "cached",
            "actual_api_called": False,
        }
    else:
        # 캐시가 없을 때만 실제 Gemini API를 호출합니다.
        ai_result = generate_ai_answer(payload.message)
        set_cached_answer(cache_key, ai_result["answer"])

    row = {
        "user_id": user["id"],
        "user_email": user["email"],
        "user_message": payload.message,
        "assistant_message": ai_result["answer"],
        "provider": ai_result["provider"],
        "model": ai_result["model"],
    }
    try:
        get_service_client().table("frontend_chat_logs").insert(row).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Supabase 테이블 'frontend_chat_logs'을 찾을 수 없습니다. "
                "backend_service/schema.sql을 Supabase SQL Editor에서 먼저 실행하세요."
            ),
        ) from exc

    add_service_log("chat", "success", "AI 응답 생성과 대화 기록 저장 완료", user)

    return ai_result


def list_conversations(user: dict[str, str]) -> list[dict]:
    """현재 사용자의 최근 대화 기록을 Supabase에서 최신순으로 조회합니다."""

    try:
        result = (
            get_service_client()
            .table("frontend_chat_logs")
            .select("id, user_message, assistant_message, provider, model, created_at")
            .eq("user_id", user["id"])
            .order("created_at", desc=True)
            .limit(50)
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Supabase 테이블 'frontend_chat_logs'을 찾을 수 없습니다. "
                "backend_service/schema.sql을 Supabase SQL Editor에서 먼저 실행하세요."
            ),
        ) from exc

    return result.data or []
