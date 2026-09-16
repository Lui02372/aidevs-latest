"""LLM 응답 생성 로직을 모아 둔 파일입니다."""

from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatWithHistoryRequest, Message


DEFAULT_PROVIDER = "gemini"
DEFAULT_MODEL = "gemini-2.5-flash-lite"


def build_prompt(message: str, memo_context: str = "", history: list[Message] | None = None) -> str:
    """TODO: 메모, 이전 대화, 현재 질문을 하나의 prompt로 구성하세요."""

    return ""


def generate_mock_answer(prompt: str) -> str:
    """TODO: 실제 API 대신 prompt를 반영한 mock 답변을 생성하세요."""

    return "TODO"


def build_messages_for_storage(
    user_message: str,
    assistant_answer: str,
    history: list[Message] | None = None,
) -> list[Message]:
    """TODO: Supabase에 저장하기 좋은 메시지 목록을 구성하세요."""

    return []


def create_single_turn_response(request: ChatRequest) -> ChatResponse:
    """TODO: single-turn 요청을 ChatResponse로 변환하세요."""

    prompt = build_prompt(message=request.message, memo_context=request.memo_context)
    answer = generate_mock_answer(prompt)

    return ChatResponse(
        provider=DEFAULT_PROVIDER,
        model=DEFAULT_MODEL,
        actual_api_called=False,
        answer=answer,
        messages_for_storage=build_messages_for_storage(request.message, answer),
    )


def create_multi_turn_response(request: ChatWithHistoryRequest) -> ChatResponse:
    """TODO: multi-turn 요청을 ChatResponse로 변환하세요."""

    prompt = build_prompt(message=request.message, history=request.history)
    answer = generate_mock_answer(prompt)

    return ChatResponse(
        provider=DEFAULT_PROVIDER,
        model=DEFAULT_MODEL,
        actual_api_called=False,
        answer=answer,
        messages_for_storage=build_messages_for_storage(request.message, answer, request.history),
    )
