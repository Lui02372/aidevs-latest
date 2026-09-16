r"""비용 없는 멀티턴 대화 예제입니다.

이전 대화를 messages 목록에 담아 다음 요청에 함께 보내는 구조를 확인합니다.
실제 API를 호출하지 않으므로 API key와 비용이 필요하지 않습니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\02_llm-api-integration\04_multi-turn-call\01_mock_multi_turn.py
"""


# 멀티턴 대화에서는 이전 질문과 답변을 messages 목록에 계속 쌓습니다.
# 모델은 이 목록을 보고 "방금 무엇을 이야기했는지"를 이어서 이해합니다.
messages = [
    {"role": "system", "content": "당신은 Python과 FastAPI를 쉽게 설명하는 학습 도우미입니다."},
    {"role": "user", "content": "FastAPI에서 Pydantic을 왜 사용하나요?"},
    {"role": "assistant", "content": "요청 데이터를 검증하고 응답 모델을 정리하는 데 사용합니다."},
    {"role": "user", "content": "그럼 메모 API에서는 어떤 부분에 도움이 되나요?"},
]


def mock_multi_turn_response(history: list[dict[str, str]]) -> str:
    """대화 이력을 보고 마지막 질문에 답하는 척하는 함수입니다."""

    last_user_message = next(
        message["content"]
        for message in reversed(history)
        if message["role"] == "user"
    )

    return (
        f"마지막 질문: {last_user_message}\n"
        "메모 API에서는 Pydantic으로 title, content, tags 같은 요청 데이터를 검증하고, "
        "response_model로 internal_note 같은 내부 값을 응답에서 제외할 수 있습니다."
    )


print("전달할 메시지 개수:", len(messages))
print("-" * 50)

for message in messages:
    print(f"{message['role']}: {message['content']}")

print()
print(mock_multi_turn_response(messages))
