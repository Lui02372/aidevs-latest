r"""비용 없는 싱글턴 LLM 호출 예제입니다.

실제 API를 호출하지 않고, LLM API 호출 흐름을 함수로 흉내 냅니다.
초보 단계에서는 먼저 입력, 파라미터, 응답 구조를 이해하는 것이 중요합니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\02_llm-api-integration\03_single-turn-call\01_mock_single_turn.py
"""


def mock_llm_response(prompt: str, temperature: float = 0.3, max_tokens: int = 200) -> dict:
    """가짜 LLM 응답을 생성합니다."""

    return {
        "provider": "mock",
        "model": "mock-teacher",
        "usage": {
            # input_length는 실제 토큰 수가 아니라 수업용 예시 값입니다.
            # 실제 서비스에서는 provider가 반환하는 token usage를 확인합니다.
            "input_length": len(prompt),
            "max_tokens": max_tokens,
        },
        "answer": (
            f"질문과 컨텍스트:\n{prompt}\n\n"
            f"temperature={temperature} 설정으로 안정적인 수업용 답변을 생성했다고 가정합니다."
        ),
    }


memo_context = "Pydantic은 요청 데이터의 타입과 길이를 검증하고, 잘못된 요청은 422 오류로 처리한다."
question = "FastAPI에서 Pydantic을 왜 사용하나요?"

prompt = (
    "당신은 Python과 FastAPI를 쉽게 설명하는 학습 도우미입니다.\n"
    f"참고 메모: {memo_context}\n"
    f"사용자 질문: {question}"
)

# 싱글턴 호출은 "현재 질문 1개 -> AI 답변 1개" 흐름입니다.
result = mock_llm_response(prompt)
print("1.----------------------------------")
print(result)
print("2.----------------------------------")
print(result["answer"])
print("3.----------------------------------")
print("\n사용량 예시:", result["usage"])
