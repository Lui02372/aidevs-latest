"""Assignment 04 starter: Multi-turn 대화 이력과 Gemini SDK 변환 설계."""

from pprint import pprint


conversation: list[dict] = []


def add_message(role: str, content: str) -> None:
    """대화 이력에 메시지를 추가합니다."""
    # TODO: role과 content를 가진 딕셔너리를 conversation에 추가하세요.


def get_recent_messages(limit: int = 4) -> list[dict]:
    """최근 메시지 일부만 반환합니다."""
    # TODO: conversation의 마지막 limit개 메시지를 반환하세요.
    return []


def build_messages_for_llm(recent_messages: list[dict]) -> list[dict]:
    """LLM 요청에 사용할 메시지 목록을 구성합니다."""
    system_message = {
        "role": "system",
        "content": "너는 이전 대화 흐름을 참고해 짧고 정확하게 답변하는 AI 비서입니다.",
    }

    # TODO: system_message 뒤에 recent_messages를 붙여 반환하세요.
    # README에는 이 구조를 Gemini contents 구조로 바꾸는 기준을 정리하세요.
    return []


def call_mock_llm(messages: list[dict]) -> dict:
    """대화 이력을 참고한 mock 응답을 만듭니다."""
    # TODO: 마지막 user 메시지를 찾아 answer에 반영하세요.
    return {}


add_message("user", "LLM API의 message 구조를 배웠어.")
add_message("assistant", "좋습니다. role과 content를 구분하는 것이 핵심입니다.")
add_message("user", "이 내용을 Supabase에 저장하려면 어떤 필드가 필요해?")

recent = get_recent_messages()
messages_for_llm = build_messages_for_llm(recent)
response = call_mock_llm(messages_for_llm)

pprint(response, width=100)
