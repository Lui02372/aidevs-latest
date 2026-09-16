"""Lab 04 starter: Multi-turn mock-first 대화 이력과 Gemini SDK 확장 준비."""

from pprint import pprint


conversation = []


def add_user_message(content: str) -> None:
    """사용자 메시지를 대화 이력에 추가합니다."""
    # TODO: role이 user인 딕셔너리를 conversation에 추가하세요.


def add_assistant_message(content: str) -> None:
    """AI 응답 메시지를 대화 이력에 추가합니다."""
    # TODO: role이 assistant인 딕셔너리를 conversation에 추가하세요.


def get_recent_messages(limit: int = 4) -> list[dict]:
    """최근 메시지 일부만 반환합니다."""
    # TODO: conversation의 마지막 limit개 메시지를 반환하세요.
    return []


def call_mock_llm_with_history(messages: list[dict]) -> dict:
    """대화 이력을 참고해 mock 응답을 만듭니다."""
    # TODO: 마지막 user 메시지를 찾아 답변에 반영하세요.
    # 이후 실제 프로젝트에서는 messages를 Gemini contents 구조로 변환한 뒤 SDK에 전달합니다.
    return {}


add_user_message("오늘 FastAPI와 Pydantic을 배웠어.")
add_assistant_message("좋습니다. 입력 검증과 API 응답 구조가 핵심입니다.")
add_user_message("그럼 LLM API와 연결할 때는 무엇을 조심해야 해?")

recent_messages = get_recent_messages()
response = call_mock_llm_with_history(recent_messages)

pprint(response, width=100)
