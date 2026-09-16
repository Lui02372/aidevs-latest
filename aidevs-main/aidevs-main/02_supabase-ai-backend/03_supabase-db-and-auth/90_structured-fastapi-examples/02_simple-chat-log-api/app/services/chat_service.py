"""Gemini AI 답변을 만들고 Supabase에 로그를 저장합니다."""

from __future__ import annotations

import os

from fastapi import HTTPException, status

from app.core.gemini import get_gemini_client
from app.core.supabase import get_supabase_client
from app.schemas.chat_schema import ChatLogPublic, ChatRequest, ChatResponse


TABLE_NAME = "ex90_simple_chat_logs"


def create_gemini_answer(message: str) -> tuple[str, str]:
    """Gemini SDK로 답변을 만듭니다."""

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    client = get_gemini_client()
    try:
        response = client.models.generate_content(model=model, contents=message)
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Gemini 호출 실패: {error}") from error

    return response.text or "", model


def to_log_public(row: dict) -> ChatLogPublic:
    """Supabase row를 API 응답 모델로 변환합니다."""

    return ChatLogPublic(
        id=str(row["id"]),
        user_message=row["user_message"],
        assistant_message=row.get("assistant_message"),
        provider=row["provider"],
        model=row.get("model"),
        actual_api_called=bool(row.get("actual_api_called", False)),
        status=row["status"],
        error_message=row.get("error_message"),
        created_at=row.get("created_at"),
    )


def answer_and_log(request: ChatRequest) -> ChatResponse:
    """Gemini 답변 생성과 로그 저장을 한 번에 수행합니다."""

    answer, model = create_gemini_answer(request.message)
    # DB에 저장할 컬럼만 명시적으로 구성합니다.
    payload = {
        "user_message": request.message,
        "assistant_message": answer,
        "provider": "gemini",
        "model": model,
        "actual_api_called": True,
        "status": "success",
    }
    supabase = get_supabase_client()

    result = supabase.table(TABLE_NAME).insert(payload).execute()

    log_id = str(result.data[0]["id"]) if result.data else None

    # API 응답은 DB 저장 결과 전체가 아니라 화면에 필요한 값만 돌려줍니다.
    return ChatResponse(
        user_message=request.message,
        assistant_message=answer,
        provider="gemini",
        model=model,
        actual_api_called=True,
        log_id=log_id,
    )


def list_logs() -> list[ChatLogPublic]:
    """최근 채팅 로그 20개를 최신순으로 조회합니다."""

    supabase = get_supabase_client()
    try:
        result = (
            supabase.table(TABLE_NAME)
            .select("*")
            .order("created_at", desc=True)
            .limit(20)
            .execute()
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Supabase 로그 조회 실패: {error}",
        ) from error
    return [to_log_public(row) for row in result.data]
