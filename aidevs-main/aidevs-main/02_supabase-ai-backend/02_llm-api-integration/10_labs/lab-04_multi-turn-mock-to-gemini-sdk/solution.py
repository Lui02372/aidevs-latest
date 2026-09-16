"""Lab 04 solution: Multi-turn mock-first 대화 이력과 Gemini SDK 확장 준비."""

from pprint import pprint


# 대화 이력은 메시지 딕셔너리를 순서대로 담는 리스트입니다.
# 실제 서비스에서는 이 리스트의 각 항목을 Supabase 테이블에 저장할 수 있습니다.
conversation = []


def add_user_message(content: str) -> None:
    """사용자 메시지를 대화 이력에 추가합니다."""
    conversation.append({"role": "user", "content": content})


def add_assistant_message(content: str) -> None:
    """AI 응답 메시지를 대화 이력에 추가합니다."""
    conversation.append({"role": "assistant", "content": content})


def get_recent_messages(limit: int = 4) -> list[dict]:
    """최근 메시지 일부만 반환합니다."""
    return conversation[-limit:]


def call_mock_llm_with_history(messages: list[dict]) -> dict:
    """대화 이력을 참고해 mock 응답을 만듭니다."""
    # 실제 프로젝트에서는 messages를 Gemini contents 구조로 변환한 뒤 SDK에 전달합니다.
    last_user_message = ""

    # 뒤에서부터 확인하면 가장 최근 사용자 메시지를 쉽게 찾을 수 있습니다.
    for message in reversed(messages):
        if message["role"] == "user":
            last_user_message = message["content"]
            break

    answer = (
        "LLM API와 연결할 때는 API key를 코드에 직접 적지 않고, "
        "실제 호출 여부와 비용 발생 가능성을 항상 확인해야 합니다. "
        f"최근 질문도 함께 보면 '{last_user_message}'에 대한 답변 흐름을 이어갈 수 있습니다."
    )

    return {
        "provider": "gemini",
        "model": "gemini-2.5-flash-lite",
        "actual_api_called": False,
        "messages_used": messages,
        "answer": answer,
    }


add_user_message("오늘 FastAPI와 Pydantic을 배웠어.")
add_assistant_message("좋습니다. 입력 검증과 API 응답 구조가 핵심입니다.")
add_user_message("그럼 LLM API와 연결할 때는 무엇을 조심해야 해?")

recent_messages = get_recent_messages()
response = call_mock_llm_with_history(recent_messages)

pprint(response, width=100)
