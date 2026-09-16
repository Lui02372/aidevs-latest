"""Lab 03 solution: Single-turn mock-first 호출과 Gemini SDK 확장 준비."""

from pprint import pprint


def estimate_tokens(text: str) -> int:
    """아주 단순하게 공백 기준으로 토큰 수를 추정합니다."""
    return len(text.split())


def build_prompt(memo_context: str, user_question: str) -> str:
    """메모 컨텍스트와 질문을 하나의 프롬프트로 합칩니다."""
    return (
        "아래 메모를 참고해서 사용자의 질문에 답변하세요.\n\n"
        f"[메모]\n{memo_context}\n\n"
        f"[질문]\n{user_question}"
    )


def call_mock_llm(prompt: str) -> dict:
    """실제 API 대신 mock 응답을 반환합니다."""
    # 실제 프로젝트에서는 이 함수 내부가 Gemini SDK generate_content 호출로 교체됩니다.
    answer = (
        "1. FastAPI는 POST 요청으로 클라이언트가 보낸 JSON 데이터를 받을 수 있습니다.\n"
        "2. Pydantic 모델을 사용하면 입력 데이터의 필드와 타입을 검증할 수 있습니다.\n"
        "3. 검증된 데이터는 API 응답 생성이나 Supabase 저장 흐름으로 이어질 수 있습니다."
    )

    return {
        "provider": "gemini",
        "model": "gemini-2.5-flash-lite",
        "actual_api_called": False,
        "prompt": prompt,
        "answer": answer,
        "usage": {
            "input_tokens_estimate": estimate_tokens(prompt),
            "output_tokens_estimate": estimate_tokens(answer),
        },
    }


memo_context = "FastAPI에서 POST 요청으로 JSON 데이터를 받는 방법을 배웠다."
user_question = "이 내용을 3줄로 복습해줘."

prompt = build_prompt(memo_context, user_question)
response = call_mock_llm(prompt)

pprint(response, width=100)
