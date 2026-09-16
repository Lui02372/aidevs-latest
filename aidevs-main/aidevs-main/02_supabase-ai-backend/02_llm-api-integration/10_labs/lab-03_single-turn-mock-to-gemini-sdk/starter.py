"""Lab 03 starter: Single-turn mock-first 호출과 Gemini SDK 확장 준비."""

from pprint import pprint


def estimate_tokens(text: str) -> int:
    """아주 단순하게 공백 기준으로 토큰 수를 추정합니다."""
    # TODO: text를 공백 기준으로 나눈 개수를 반환하세요.
    return 0


def build_prompt(memo_context: str, user_question: str) -> str:
    """메모 컨텍스트와 질문을 하나의 프롬프트로 합칩니다."""
    # TODO: AI가 참고할 수 있도록 memo_context와 user_question을 함께 반환하세요.
    return ""


def call_mock_llm(prompt: str) -> dict:
    """실제 API 대신 mock 응답을 반환합니다."""
    # TODO: provider, model, actual_api_called, answer, usage를 포함한 딕셔너리를 반환하세요.
    # 이후 실제 프로젝트에서는 이 함수 위치가 Gemini SDK 호출 함수로 바뀝니다.
    return {}


memo_context = "FastAPI에서 POST 요청으로 JSON 데이터를 받는 방법을 배웠다."
user_question = "이 내용을 3줄로 복습해줘."

prompt = build_prompt(memo_context, user_question)
response = call_mock_llm(prompt)

pprint(response, width=100)
