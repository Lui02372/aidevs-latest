from time import sleep
from uuid import uuid4

from app.core.config import ENABLE_FAKE_DELAY
from app.schemas.chat_schema import ChatRequest
from app.services.log_service import add_log, now_text
from app.services.memory_store import conversations


def build_mock_answer(user_email: str, message: str) -> str:
    """실제 LLM 대신 사용할 수업용 답변 문자열을 만듭니다.

    최근 대화가 있으면 "이전 대화를 참고한다"는 힌트를 붙여,
    프론트엔드에서 연속 대화처럼 보이는 흐름을 연습할 수 있게 합니다.
    """

    recent = [
        item
        for item in conversations
        if item["user_email"] == user_email
    ][-3:]

    context_hint = ""
    if recent:
        context_hint = f" 이전 대화 {len(recent)}개를 참고해 이어서 답변합니다."

    return f"'{message}'에 대한 수업용 mock AI 답변입니다.{context_hint}"


def create_chat(user: dict, payload: ChatRequest) -> dict:
    """사용자 질문을 받아 mock 답변을 만들고 대화 기록에 저장합니다."""

    if ENABLE_FAKE_DELAY:
        # 로딩 UI를 테스트하고 싶을 때만 짧게 대기합니다.
        sleep(0.5)

    answer = build_mock_answer(user["email"], payload.message)
    item = {
        "id": str(uuid4()),
        "user_email": user["email"],
        "user_message": payload.message,
        "assistant_message": answer,
        "created_at": now_text(),
    }
    conversations.append(item)

    # 서비스 로그를 남기면 프론트엔드의 운영 로그 화면에서 확인할 수 있습니다.
    add_log("chat", "success", "mock AI 답변 생성", user["email"])

    return {
        "conversation_id": item["id"],
        "answer": answer,
        "actual_api_called": False,
        "provider": "mock",
        "model": "mock-chat-ux-v1",
    }


def list_conversations_for_user(user_email: str) -> list[dict]:
    """특정 사용자의 대화 기록만 최신순으로 반환합니다."""

    return [
        item
        for item in reversed(conversations)
        if item["user_email"] == user_email
    ]
