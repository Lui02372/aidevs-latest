"""LLM 응답 생성 로직을 모아 둔 solution 파일입니다."""

from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatWithHistoryRequest, Message


DEFAULT_PROVIDER = "gemini"
DEFAULT_MODEL = "gemini-2.5-flash-lite"


def build_prompt(message: str, memo_context: str = "", history: list[Message] | None = None) -> str:
    """메모, 이전 대화, 현재 질문을 하나의 prompt로 구성합니다."""

    parts = ["당신은 Python과 FastAPI를 쉽게 설명하는 학습 도우미입니다."]

    if memo_context:
        parts.append(f"참고 메모:\n{memo_context}")

    if history:
        history_lines = [f"{item.role}: {item.content}" for item in history]
        parts.append("이전 대화:\n" + "\n".join(history_lines))

    parts.append(f"사용자 질문:\n{message}")
    parts.append("답변은 초보자가 이해할 수 있도록 짧고 명확하게 작성합니다.")

    return "\n\n".join(parts)


def generate_mock_answer(prompt: str) -> str:
    """실제 API 대신 prompt를 반영한 mock 답변을 생성합니다."""

    preview = prompt.replace("\n", " ")[:180]
    return f"mock 답변입니다. 요청 내용을 요약하면 다음과 같습니다: {preview}"


def build_messages_for_storage(
    user_message: str,
    assistant_answer: str,
    history: list[Message] | None = None,
) -> list[Message]:
    """Supabase에 저장하기 좋은 메시지 목록을 구성합니다."""

    messages = list(history or [])
    messages.append(Message(role="user", content=user_message))
    messages.append(Message(role="assistant", content=assistant_answer))
    return messages


def create_single_turn_response(request: ChatRequest) -> ChatResponse:
    """single-turn 요청을 ChatResponse로 변환합니다."""

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
    """multi-turn 요청을 ChatResponse로 변환합니다."""

    prompt = build_prompt(message=request.message, history=request.history)
    answer = generate_mock_answer(prompt)

    return ChatResponse(
        provider=DEFAULT_PROVIDER,
        model=DEFAULT_MODEL,
        actual_api_called=False,
        answer=answer,
        messages_for_storage=build_messages_for_storage(request.message, answer, request.history),
    )
