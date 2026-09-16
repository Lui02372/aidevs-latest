"""이전 대화를 읽어 Gemini 멀티턴 질문을 처리합니다."""

import os
from uuid import uuid4

from fastapi import HTTPException, status

from app.core.gemini import get_gemini_client
from app.core.supabase import get_supabase_client
from app.schemas.chat_schema import ChatMessage, ChatRequest, ChatResponse


TABLE_NAME = "ex90_multi_turn_chat_logs"
HISTORY_LIMIT = 6


def to_chat_message(row: dict) -> ChatMessage:
    """Supabase row를 API 응답 모델로 바꿉니다."""

    return ChatMessage(
        id=str(row["id"]),
        conversation_id=str(row["conversation_id"]),
        user_message=row["user_message"],
        assistant_message=row["assistant_message"],
        model=row["model"],
        created_at=row.get("created_at"),
    )


def get_recent_history(conversation_id: str) -> list[dict]:
    """현재 대화의 최근 질문/답변을 오래된 순서로 가져옵니다."""

    supabase = get_supabase_client()
    try:
        result = (
            supabase.table(TABLE_NAME)
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=True)
            .limit(HISTORY_LIMIT)
            .execute()
        )
    except Exception as error:
        raise HTTPException(500, f"대화 이력 조회 실패: {error}") from error

    return list(reversed(result.data))


def make_prompt(history: list[dict], message: str) -> str:
    """이전 대화와 새 질문을 Gemini에 보낼 텍스트로 만듭니다."""

    lines = ["당신은 초보자에게 쉽게 설명하는 AI 도우미입니다."]
    for row in history:
        lines.append(f"사용자: {row['user_message']}")
        lines.append(f"AI: {row['assistant_message']}")
    lines.append(f"사용자: {message}")
    lines.append("AI:")
    return "\n".join(lines)


def create_gemini_answer(prompt: str) -> tuple[str, str]:
    """Gemini SDK로 답변을 만듭니다."""

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    client = get_gemini_client()
    try:
        response = client.models.generate_content(model=model, contents=prompt)
    except Exception as error:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, f"Gemini 호출 실패: {error}") from error

    return response.text or "", model


def save_turn(conversation_id: str, message: str, answer: str, model: str) -> None:
    """새 질문과 답변을 한 턴으로 저장합니다."""

    supabase = get_supabase_client()
    try:
        supabase.table(TABLE_NAME).insert(
            {
                "conversation_id": conversation_id,
                "user_message": message,
                "assistant_message": answer,
                "model": model,
            }
        ).execute()
    except Exception as error:
        raise HTTPException(500, f"대화 저장 실패: {error}") from error


def chat(request: ChatRequest) -> ChatResponse:
    """이전 대화를 문맥으로 사용해 새 답변을 만들고 저장합니다."""

    conversation_id = str(request.conversation_id) if request.conversation_id else str(uuid4())
    history = get_recent_history(conversation_id)
    answer, model = create_gemini_answer(make_prompt(history, request.message))
    save_turn(conversation_id, request.message, answer, model)

    return ChatResponse(
        conversation_id=conversation_id,
        user_message=request.message,
        assistant_message=answer,
        model=model,
        context_turns=len(history),
    )


def list_messages(conversation_id: str) -> list[ChatMessage]:
    """대화 전체 이력을 오래된 순서로 반환합니다."""

    supabase = get_supabase_client()
    try:
        result = (
            supabase.table(TABLE_NAME)
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at")
            .execute()
        )
    except Exception as error:
        raise HTTPException(500, f"대화 이력 조회 실패: {error}") from error

    return [to_chat_message(row) for row in result.data]
